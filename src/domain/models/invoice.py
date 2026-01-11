from datetime import datetime
from typing import Optional

class Invoice:
    """Domain entity representing an invoice"""
    
    def __init__(
        self,
        id: Optional[int],
        invoice_number: str,
        customer_name: str,
        invoice_type: str = 'SALES',
        total_amount: float = 0.0,
        discount_total: float = 0.0,
        vat_total: float = 0.0,
        description: str = None,
        status: str = 'DRAFT',
        source: str = 'MANUAL',
        created_by: int = None,
        household_id: Optional[int] = None,
        created_at: datetime = None,
        updated_at: datetime = None
    ):
        self.id = id
        self.invoice_number = invoice_number
        self.customer_name = customer_name
        self.invoice_type = invoice_type
        self.total_amount = total_amount
        self.discount_total = discount_total
        self.vat_total = vat_total
        self.description = description
        self.status = status  # DRAFT, CONFIRMED, PAID, CANCELLED
        self.source = source  # MANUAL, AI
        self.created_by = created_by
        self.household_id = household_id
        self.created_at = created_at
        self.updated_at = updated_at
