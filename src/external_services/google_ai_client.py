"""
Google AI Studio Client
Wrapper for Google Generative AI (Gemini) API
Handles API calls, prompt engineering, and response parsing for invoice creation
"""

import google.genai as genai
from typing import Dict, Any, Optional, List
import json
import re
from config import Config


class GoogleAIClient:
    """
    Client for Google AI Studio API (Gemini)
    Handles API calls and response parsing for AI-powered invoice creation
    """
    
    def __init__(self, api_key: str = None, model: str = None):
        """
        Initialize Google AI client
        
        Args:
            api_key: Google AI API key (defaults to Config.GOOGLE_AI_API_KEY)
            model: Model name (defaults to Config.GOOGLE_AI_MODEL)
        """
        self.api_key = api_key or Config.GOOGLE_AI_API_KEY
        self.model_name = model or Config.GOOGLE_AI_MODEL
        
        if not self.api_key:
            raise ValueError("Google AI API key is required. Set GOOGLE_AI_API_KEY in .env file")
        
        # Initialize client - google.genai style
        self.client = genai.Client(api_key=self.api_key)
    
    def generate_content(
        self,
        prompt: str,
        temperature: float = None,
        max_tokens: int = None
    ) -> str:
        """
        Call Gemini API with prompt
        
        Args:
            prompt: Input prompt
            temperature: Sampling temperature (0-1, lower = more deterministic)
            max_tokens: Maximum output tokens
            
        Returns:
            Generated text response
        """
        temperature = temperature if temperature is not None else Config.GOOGLE_AI_TEMPERATURE
        max_tokens = max_tokens if max_tokens is not None else Config.GOOGLE_AI_MAX_TOKENS
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=genai.types.GenerateContentConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens,
                )
            )
            return response.text
        except Exception as e:
            raise ValueError(f"Error calling Google AI API: {str(e)}")
    
    def parse_invoice_from_text(
        self,
        user_input: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Parse natural language to structured invoice data
        
        Args:
            user_input: Natural language command (Vietnamese)
            context: {
                'products': [{'id': int, 'name': str, 'price': float}, ...],
                'customers': [{'id': int, 'name': str, 'phone': str}, ...],
                'units': [{'id': int, 'name': str}, ...],
                'household_id': int
            }
        
        Returns:
            {
                'customer_name': str or None,
                'invoice_type': 'PAID' or 'UNPAID',
                'items': [
                    {
                        'product_name': str,
                        'quantity': float,
                        'unit_name': str (optional)
                    },
                    ...
                ]
            }
        """
        prompt = self._build_invoice_prompt(user_input, context)
        response_text = self.generate_content(prompt, temperature=0.2)
        return self._parse_json_response(response_text)
    
    def _build_invoice_prompt(
        self,
        user_input: str,
        context: Dict[str, Any]
    ) -> str:
        """
        Build prompt for invoice parsing with context
        
        Args:
            user_input: User's natural language command
            context: Available products, customers, units
            
        Returns:
            Complete prompt string
        """
        # Format products list
        products_list = "\n".join([
            f"- {p['name']}"
            for p in context.get('products', [])[:200]  # Limit to 200 products to avoid token limit
        ])
        
        # Format customers list
        customers_list = "\n".join([
            f"- {c['name']}" + (f" ({c['phone']})" if c.get('phone') else "")
            for c in context.get('customers', [])[:200]  # Limit to 200 customers
        ])
        
        # Format units list
        units_list = "\n".join([
            f"- {u['name']}"
            for u in context.get('units', [])
        ])
        
        prompt = f"""Bạn là trợ lý AI chuyên phân tích lệnh tiếng Việt để tạo hóa đơn bán hàng vật liệu xây dựng.

NHIỆM VỤ:
Phân tích câu lệnh của người dùng và trả về JSON với cấu trúc sau:

{{
  "customer_name": "tên khách hàng hoặc null",
  "invoice_type": "PAID hoặc UNPAID",
  "items": [
    {{
      "product_name": "tên sản phẩm",
      "quantity": số lượng (số thực),
      "unit_name": "đơn vị (nếu có)"
    }}
  ]
}}

QUY TẮC:
1. Nếu có từ "ghi nợ", "nợ", "chịu", "trả sau" → invoice_type = "UNPAID"
2. Nếu có từ "tiền mặt", "thanh toán", "trả tiền", "trả ngay" → invoice_type = "PAID"
3. Mặc định: invoice_type = "PAID"
4. Tên khách hàng: anh/chị/ông/bà/cô/chú + tên (ví dụ: "anh Nam", "chị Lan")
5. Nếu không có tên khách hàng, để customer_name = null
6. Số lượng: số + đơn vị đếm (bao, cây, kg, tấn, m3, ...)
7. Sản phẩm: tìm tên gần đúng nhất trong danh sách sản phẩm có sẵn
8. Nếu không tìm thấy sản phẩm chính xác, chọn sản phẩm gần nghĩa nhất
9. Nếu không có đơn vị, để unit_name = null

DANH SÁCH SẢN PHẨM CÓ SẴN:
{products_list if products_list else "Không có sản phẩm"}

DANH SÁCH KHÁCH HÀNG:
{customers_list if customers_list else "Không có khách hàng"}

DANH SÁCH ĐƠN VỊ:
{units_list if units_list else "Không có đơn vị"}

CÂU LỆNH CỦA NGƯỜI DÙNG:
"{user_input}"

CHỈ TRẢ VỀ JSON, KHÔNG GIẢI THÍCH. JSON phải hợp lệ và có thể parse được.
"""
        return prompt
    
    def _parse_json_response(self, response_text: str) -> Dict[str, Any]:
        """
        Parse JSON from AI response
        Handles markdown code blocks and extracts JSON
        
        Args:
            response_text: Raw response from AI
            
        Returns:
            Parsed JSON dict
        """
        # Try to extract JSON from markdown code blocks
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(1)
        else:
            # Try to find JSON object directly
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
            else:
                json_str = response_text
        
        try:
            result = json.loads(json_str)
            
            # Validate structure
            if not isinstance(result, dict):
                raise ValueError("Response is not a JSON object")
            
            if 'items' not in result or not isinstance(result['items'], list):
                raise ValueError("Missing or invalid 'items' field")
            
            # Set defaults
            if 'customer_name' not in result:
                result['customer_name'] = None
            if 'invoice_type' not in result:
                result['invoice_type'] = 'PAID'
            
            # Validate invoice_type
            if result['invoice_type'] not in ['PAID', 'UNPAID']:
                result['invoice_type'] = 'PAID'
            
            return result
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON from AI response: {str(e)}\nResponse: {response_text}")
