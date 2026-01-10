from domain.models.invoice import Invoice
from domain.models.iinvoice_repository import IInvoiceRepository
from typing import List, Optional
from datetime import datetime
import random
import string

class InvoiceService:
    """Business logic for invoice management"""
    
    def __init__(self, repository: IInvoiceRepository):
        self.repository = repository
    
    def create_invoice(
        self,
        customer_name: str,
        total_amount: float,
        status: str,
        source: str,
        created_by: int
    ) -> Invoice:
        """Create a new invoice with auto-generated invoice number"""
        now = datetime.utcnow()
        invoice_number = self._generate_invoice_number()
        
        invoice = Invoice(
            id=None,
            invoice_number=invoice_number,
            customer_name=customer_name,
            total_amount=total_amount,
            status=status,
            source=source,
            created_by=created_by,
            created_at=now,
            updated_at=now
        )
        return self.repository.create(invoice)
    
    def get_invoice(self, invoice_id: int) -> Optional[Invoice]:
        """Get invoice by ID"""
        return self.repository.get_by_id(invoice_id)
    
    def list_all_invoices(self) -> List[Invoice]:
        """List all invoices (Owner only)"""
        return self.repository.list_all()
    
    def list_user_invoices(self, user_id: int) -> List[Invoice]:
        """List invoices for specific user (Employee)"""
        return self.repository.list_by_user(user_id)
    
    def list_draft_orders(self) -> List[Invoice]:
        """List draft orders from AI"""
        return self.repository.list_draft_orders()
    
    def update_invoice(
        self,
        invoice_id: int,
        customer_name: str,
        total_amount: float,
        status: str
    ) -> Invoice:
        """Update an existing invoice (only if status is DRAFT)"""
        existing_invoice = self.repository.get_by_id(invoice_id)
        if not existing_invoice:
            raise ValueError('Invoice not found')
        
        if existing_invoice.status != 'DRAFT':
            raise ValueError('Only draft invoices can be updated')
        
        existing_invoice.customer_name = customer_name
        existing_invoice.total_amount = total_amount
        existing_invoice.status = status
        existing_invoice.updated_at = datetime.utcnow()
        
        return self.repository.update(existing_invoice)
    
    def delete_invoice(self, invoice_id: int) -> None:
        """Delete an invoice"""
        self.repository.delete(invoice_id)
    
    def confirm_invoice(self, invoice_id: int) -> Invoice:
        """Confirm a draft invoice"""
        return self.repository.confirm(invoice_id)
    
    def _generate_invoice_number(self) -> str:
        """Generate unique invoice number in format INV-YYYYMMDD-XXXX"""
        date_str = datetime.utcnow().strftime('%Y%m%d')
        random_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
        return f'INV-{date_str}-{random_str}'
