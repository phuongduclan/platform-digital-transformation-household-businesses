from datetime import datetime
from decimal import Decimal
from typing import Optional

class InvoiceDetail:
    def __init__(self, id: int = None, invoice_id: int = None, product_id: int = None,
                 unit_id: int = None, vat: int = None, discount: int = None,
                 price: Decimal = None, description: str = None, quantity: int = None,
                 status: str = None, created_at: datetime = None, updated_at: datetime = None):
        self.id = id
        self.invoice_id = invoice_id
        self.product_id = product_id
        self.unit_id = unit_id
        self.vat = vat
        self.discount = discount
        self.price = price
        self.description = description
        self.quantity = quantity
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
