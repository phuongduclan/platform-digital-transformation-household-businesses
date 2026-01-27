"""
AI Invoice Service
Orchestrates AI-powered invoice creation from natural language
Handles: AI parsing → Entity matching → Validation → Invoice creation
"""

from external_services.google_ai_client import GoogleAIClient
from services.invoice_service import InvoiceService
from services.product_service import ProductService
from services.customer_service import CustomerService
from services.unit_service import UnitService
from typing import Dict, Any, Optional, List
import re
from fuzzywuzzy import fuzz, process

# Fuzzy matching thresholds
FUZZY_MATCH_THRESHOLD_HIGH = 85  # For exact-like matches
FUZZY_MATCH_THRESHOLD_MEDIUM = 70  # For good matches
FUZZY_MATCH_THRESHOLD_LOW = 60  # Minimum acceptable match


class AIInvoiceService:
    """
    Service for AI-powered invoice creation
    Orchestrates: AI parsing → Data validation → Invoice creation
    """
    
    def __init__(
        self,
        ai_client: GoogleAIClient,
        invoice_service: InvoiceService,
        product_service: ProductService,
        customer_service: CustomerService,
        unit_service: UnitService
    ):
        self.ai_client = ai_client
        self.invoice_service = invoice_service
        self.product_service = product_service
        self.customer_service = customer_service
        self.unit_service = unit_service
    
    def create_draft_invoice_from_text(
        self,
        user_input: str,
        household_id: int,
        created_by: str = None
    ) -> Dict[str, Any]:
        """
        Main method: Convert natural language to draft invoice
        
        Args:
            user_input: Natural language command (Vietnamese)
            household_id: Household ID
            created_by: User who created this invoice
        
        Returns:
            {
                'invoice': Invoice object,
                'confidence': float (0-1),
                'warnings': [str] (if any ambiguities),
                'ai_result': dict (original AI parsing result)
            }
        """
        # 1. Load context (products, customers, units)
        context = self._load_context(household_id)
        
        # 2. Call AI to parse user input
        ai_result = self.ai_client.parse_invoice_from_text(user_input, context)
        
        # 3. Validate and match entities
        validated_data = self._validate_and_match(ai_result, context, household_id)
        
        # 4. Create draft invoice
        invoice = self.invoice_service.create_invoice_with_details(
            household_id=household_id,
            customer_id=validated_data.get('customer_id'),
            invoice_type=validated_data.get('invoice_type', 'PAID'),
            description=f"AI Draft: {user_input[:100]}",
            status='Draft',
            created_by=created_by,
            details=validated_data['details']
        )
        
        return {
            'invoice': invoice,
            'confidence': validated_data.get('confidence', 0.8),
            'warnings': validated_data.get('warnings', []),
            'ai_result': ai_result
        }
    
    def _load_context(self, household_id: int) -> Dict[str, Any]:
        """
        Load products, customers, units for AI context
        
        Args:
            household_id: Household ID
            
        Returns:
            Context dict with products, customers, units
        """
        products = self.product_service.list_products(household_id, status='ACTIVE')
        # Fix: Customers use 'Active' (Title case) in DB, while others use 'ACTIVE'
        customers = self.customer_service.list_customers(household_id, status='Active')
        units = self.unit_service.list_units(household_id, status='ACTIVE')
        
        # DEBUG: Log customer data
        print(f"\n=== DEBUG: Loading context for household_id={household_id} ===")
        print(f"Found {len(customers)} ACTIVE customers:")
        for c in customers:
            print(f"  - ID={c.id}: '{c.name}' (phone: {c.phone})")
        print("===\n")
        
        return {
            'household_id': household_id,
            'products': [
                {'id': p.id, 'name': p.name}
                for p in products
            ],
            'customers': [
                {'id': c.id, 'name': c.name, 'phone': c.phone}
                for c in customers
            ],
            'units': [
                {'id': u.id, 'name': u.name}
                for u in units
            ]
        }
    
    def _validate_and_match(
        self,
        ai_result: Dict[str, Any],
        context: Dict[str, Any],
        household_id: int
    ) -> Dict[str, Any]:
        """
        Validate AI result and match to actual database entities
        
        Args:
            ai_result: Parsed result from AI
            context: Available products, customers, units
            household_id: Household ID
        
        Returns:
            {
                'customer_id': int or None,
                'invoice_type': str,
                'details': [...],
                'confidence': float,
                'warnings': [str]
            }
        """
        warnings = []
        
        # Match customer
        customer_id = None
        if ai_result.get('customer_name'):
            # DEBUG: Log AI result for customer
            print(f"\n=== DEBUG: Customer Matching ===")
            print(f"AI returned customer_name: '{ai_result['customer_name']}'")
            print(f"Available customers: {[c['name'] for c in context['customers']]}")
            
            customer_id, match_score = self._match_customer(
                ai_result['customer_name'],
                context['customers']
            )
            
            print(f"Match result: customer_id={customer_id}, score={match_score}")
            print("===\n")
            
            if not customer_id:
                warnings.append(f"Không tìm thấy khách hàng: {ai_result['customer_name']}")
            elif match_score < FUZZY_MATCH_THRESHOLD_HIGH:
                warnings.append(f"Khách hàng không chính xác 100% (độ tin cậy: {match_score}%)")
        
        # Match products and build details
        details = []
        for item in ai_result.get('items', []):
            product_match, match_score = self._match_product(
                item['product_name'],
                context['products']
            )
            
            if not product_match:
                warnings.append(f"Không tìm thấy sản phẩm: {item['product_name']}")
                continue
            
            if match_score < FUZZY_MATCH_THRESHOLD_HIGH:
                warnings.append(f"Sản phẩm '{item['product_name']}' → '{product_match['name']}' (độ tin cậy: {match_score}%)")
            
            # Match unit
            unit_id = None
            if item.get('unit_name'):
                unit_id, unit_match_score = self._match_unit(item['unit_name'], context['units'])
                if not unit_id:
                    warnings.append(f"Không tìm thấy đơn vị: {item['unit_name']}, dùng đơn vị mặc định")
            
            if not unit_id and context['units']:
                unit_id = context['units'][0]['id']  # Default first unit
            
            if not unit_id:
                warnings.append(f"Không có đơn vị cho sản phẩm: {product_match['name']}")
                continue
            
            details.append({
                'product_id': product_match['id'],
                'unit_id': unit_id,
                'quantity': item['quantity'],
                'price': 0,  # Price will be entered by user or fetched from inventory
                'vat': 0,
                'discount': 0,
                'description': f"AI: {item['product_name']}"
            })
        
        if not details:
            raise ValueError("Không thể tạo hóa đơn: Không tìm thấy sản phẩm nào hợp lệ")
        
        # Determine invoice type
        invoice_type = ai_result.get('invoice_type', 'PAID')
        if invoice_type == 'UNPAID' and not customer_id:
            warnings.append("Không thể ghi nợ khi không có khách hàng, chuyển sang PAID")
            invoice_type = 'PAID'
        
        # Calculate confidence
        confidence = self._calculate_confidence(ai_result, warnings)
        
        return {
            'customer_id': customer_id,
            'invoice_type': invoice_type,
            'details': details,
            'confidence': confidence,
            'warnings': warnings
        }
    
    def _match_customer(self, name: str, customers: List[Dict]) -> tuple[Optional[int], int]:
        """
        Fuzzy match customer name using fuzzywuzzy
        
        Args:
            name: Customer name from AI
            customers: List of available customers
            
        Returns:
            Tuple of (Customer ID or None, match score 0-100)
        """
        if not name or not customers:
            return None, 0
        
        # Helper to normalize name (remove prefixes)
        def normalize_name(n: str) -> str:
            n = n.lower().strip()
            prefixes = ['anh ', 'chị ', 'cô ', 'chú ', 'bác ', 'ông ', 'bà ', 'em ']
            for prefix in prefixes:
                if n.startswith(prefix):
                    return n[len(prefix):].strip()
            return n

        name_lower = name.lower().strip()
        name_normalized = normalize_name(name)
        
        # 1. Exact match first (100% confidence)
        for c in customers:
            c_name_lower = c['name'].lower().strip()
            if c_name_lower == name_lower or c_name_lower == name_normalized:
                return c['id'], 100
        
        # Use fuzzywuzzy for intelligent matching
        customer_names = {c['name']: c['id'] for c in customers}
        
        # 2. Try match with original name
        best_match_original = process.extractOne(
            name,
            customer_names.keys(),
            scorer=fuzz.token_set_ratio
        )
        
        # 3. Try match with normalized name (if different)
        best_match_normalized = None
        if name_normalized != name_lower:
            best_match_normalized = process.extractOne(
                name_normalized,
                customer_names.keys(),
                scorer=fuzz.token_set_ratio
            )
        
        # Compare and pick best match
        best_match = best_match_original
        if best_match_normalized and best_match_normalized[1] > (best_match_original[1] if best_match_original else 0):
            best_match = best_match_normalized
            
        if best_match and best_match[1] >= FUZZY_MATCH_THRESHOLD_MEDIUM:
            return customer_names[best_match[0]], best_match[1]
        
        # Try partial_ratio as fallback
        best_match_partial = process.extractOne(
            name_normalized,
            customer_names.keys(),
            scorer=fuzz.partial_ratio
        )
        
        if best_match_partial and best_match_partial[1] >= FUZZY_MATCH_THRESHOLD_HIGH:
            return customer_names[best_match_partial[0]], best_match_partial[1]
        
        return None, 0
    
    def _match_product(self, name: str, products: List[Dict]) -> tuple[Optional[Dict], int]:
        """
        Fuzzy match product name using fuzzywuzzy with multiple scoring methods
        
        Args:
            name: Product name from AI
            products: List of available products
            
        Returns:
            Tuple of (Product dict or None, match score 0-100)
        """
        if not name or not products:
            return None, 0
        
        name_lower = name.lower().strip()
        
        # Exact match first (100% confidence)
        for p in products:
            if p['name'].lower().strip() == name_lower:
                return p, 100
        
        # Build product name to object mapping
        product_map = {p['name']: p for p in products}
        
        # Try multiple fuzzy matching strategies and pick best overall
        
        # 1. Token sort ratio (handles word order: "xi măng" vs "măng xi")
        match_token_sort = process.extractOne(
            name,
            product_map.keys(),
            scorer=fuzz.token_sort_ratio
        )
        
        # 2. Token set ratio (handles extra words: "xi măng PCB40" vs "xi măng")
        match_token_set = process.extractOne(
            name,
            product_map.keys(),
            scorer=fuzz.token_set_ratio
        )
        
        # 3. Partial ratio (substring matching: "sắt" in "sắt phi 10")
        match_partial = process.extractOne(
            name,
            product_map.keys(),
            scorer=fuzz.partial_ratio
        )
        
        # Pick best match across all methods
        candidates = []
        if match_token_sort and match_token_sort[1] >= FUZZY_MATCH_THRESHOLD_LOW:
            candidates.append((match_token_sort[0], match_token_sort[1], 'token_sort'))
        if match_token_set and match_token_set[1] >= FUZZY_MATCH_THRESHOLD_LOW:
            candidates.append((match_token_set[0], match_token_set[1], 'token_set'))
        if match_partial and match_partial[1] >= FUZZY_MATCH_THRESHOLD_HIGH:
            candidates.append((match_partial[0], match_partial[1], 'partial'))
        
        if not candidates:
            return None, 0
        
        # Sort by score descending
        candidates.sort(key=lambda x: x[1], reverse=True)
        best_product_name = candidates[0][0]
        best_score = candidates[0][1]
        
        # Only return if score is above medium threshold
        if best_score >= FUZZY_MATCH_THRESHOLD_MEDIUM:
            return product_map[best_product_name], best_score
        
        return None, best_score
    
    def _match_unit(self, name: str, units: List[Dict]) -> tuple[Optional[int], int]:
        """
        Fuzzy match unit name using fuzzywuzzy
        Handles common abbreviations and variations
        
        Args:
            name: Unit name from AI
            units: List of available units
            
        Returns:
            Tuple of (Unit ID or None, match score 0-100)
        """
        if not name or not units:
            return None, 0
        
        name_lower = name.lower().strip()
        
        # Exact match first (100% confidence)
        for u in units:
            if u['name'].lower().strip() == name_lower:
                return u['id'], 100
        
        # Use fuzzywuzzy for fuzzy matching
        unit_names = {u['name']: u['id'] for u in units}
        
        # Try partial_ratio for abbreviations (e.g., "kg" in "kilogram")
        best_match = process.extractOne(
            name,
            unit_names.keys(),
            scorer=fuzz.partial_ratio
        )
        
        if best_match and best_match[1] >= FUZZY_MATCH_THRESHOLD_HIGH:
            return unit_names[best_match[0]], best_match[1]
        
        # Try token_set_ratio for variations
        best_match = process.extractOne(
            name,
            unit_names.keys(),
            scorer=fuzz.token_set_ratio
        )
        
        if best_match and best_match[1] >= FUZZY_MATCH_THRESHOLD_MEDIUM:
            return unit_names[best_match[0]], best_match[1]
        
        return None, 0
    
    def _calculate_confidence(self, ai_result: Dict, warnings: List[str]) -> float:
        """
        Calculate confidence score based on AI result and warnings
        
        Args:
            ai_result: Parsed result from AI
            warnings: List of warnings
            
        Returns:
            Confidence score (0-1)
        """
        base_confidence = 0.9
        
        # Decrease confidence for each warning
        confidence = base_confidence - (len(warnings) * 0.10)
        
        # Bonus if customer found
        if ai_result.get('customer_name') and not any('khách hàng' in w.lower() for w in warnings):
            confidence += 0.05
        
        # Minimum confidence
        return max(min(confidence, 1.0), 0.3)
