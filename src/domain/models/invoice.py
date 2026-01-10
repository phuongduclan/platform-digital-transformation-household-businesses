from datetime import datetime
from typing import Optional

class Invoice:
    """Domain entity representing an invoice"""
    
    def __init__(
        self,
        id: Optional[int],
        invoice_number: str,
        customer_name: str,
        total_amount: float,
        status: str,
        source: str,
        created_by: int,
        created_at: datetime,
        updated_at: datetime
    ):
        self.id = id
        self.invoice_number = invoice_number
        self.customer_name = customer_name
        self.total_amount = total_amount
        self.status = status  # DRAFT, CONFIRMED, PAID, CANCELLED
        self.source = source  # MANUAL, AI
        self.created_by = created_by
        self.created_at = created_at
        self.updated_at = updated_at
