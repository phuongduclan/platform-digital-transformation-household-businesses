from domain.models.invoice_detail import InvoiceDetail
from domain.models.iinvoice_detail_repository import IInvoiceDetailRepository
from typing import List, Optional

class InvoiceDetailService:
    """Business logic for invoice detail management"""
    
    def __init__(self, repository: IInvoiceDetailRepository):
        self.repository = repository
    
    def create_detail(
        self,
        invoice_id: int,
        product_name: str,
        quantity: int,
        unit_price: float,
        vat: float = 0.0,
        discount: float = 0.0,
        description: str = None
    ) -> InvoiceDetail:
        """Create a new invoice detail with auto-calculated subtotal"""
        if quantity <= 0:
            raise ValueError('Quantity must be greater than 0')
        
        if unit_price < 0:
            raise ValueError('Unit price cannot be negative')
        
        subtotal = quantity * unit_price
        
        detail = InvoiceDetail(
            id=None,
            invoice_id=invoice_id,
            product_name=product_name,
            quantity=quantity,
            unit_price=unit_price,
            vat=vat,
            discount=discount,
            description=description,
            subtotal=subtotal
        )
        return self.repository.create(detail)
    
    def get_detail(self, detail_id: int) -> Optional[InvoiceDetail]:
        """Get invoice detail by ID"""
        return self.repository.get_by_id(detail_id)
    
    def list_invoice_details(self, invoice_id: int) -> List[InvoiceDetail]:
        """List all details for a specific invoice"""
        return self.repository.list_by_invoice(invoice_id)
    
    def update_detail(
        self,
        detail_id: int,
        product_name: str,
        quantity: int,
        unit_price: float,
        vat: float = 0.0,
        discount: float = 0.0,
        description: str = None
    ) -> InvoiceDetail:
        """Update an existing invoice detail"""
        existing_detail = self.repository.get_by_id(detail_id)
        if not existing_detail:
            raise ValueError('Invoice detail not found')
        
        if quantity <= 0:
            raise ValueError('Quantity must be greater than 0')
        
        if unit_price < 0:
            raise ValueError('Unit price cannot be negative')
        
        existing_detail.product_name = product_name
        existing_detail.quantity = quantity
        existing_detail.unit_price = unit_price
        existing_detail.vat = vat
        existing_detail.discount = discount
        existing_detail.description = description
        existing_detail.subtotal = quantity * unit_price
        
        return self.repository.update(existing_detail)
    
    def delete_detail(self, detail_id: int) -> None:
        """Delete an invoice detail"""
        self.repository.delete(detail_id)
