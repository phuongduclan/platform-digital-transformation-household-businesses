from typing import Optional

class InvoiceDetail:
    """Domain entity representing an invoice line item"""
    
    def __init__(
        self,
        id: Optional[int],
        invoice_id: int,
        product_name: str,
        quantity: int,
        unit_price: float,
        subtotal: float
    ):
        self.id = id
        self.invoice_id = invoice_id
        self.product_name = product_name
        self.quantity = quantity
        self.unit_price = unit_price
        self.subtotal = subtotal
