from datetime import datetime
from decimal import Decimal
from typing import Optional

class Invoice:
    def __init__(self, id: int = None, household_id: int = None, seller_id: int = None,
                 customer_id: int = None, invoice_type: str = None, discount_total: Decimal = None,
                 vat_total: Decimal = None, total_amount: Decimal = None, description: str = None,
                 status: str = None, created_by: str = None, updated_by: str = None,
                 created_at: datetime = None, updated_at: datetime = None):
        self.id = id
        self.household_id = household_id
        self.seller_id = seller_id
        self.customer_id = customer_id
        self.invoice_type = invoice_type
        self.discount_total = discount_total
        self.vat_total = vat_total
        self.total_amount = total_amount
        self.description = description
        self.status = status
        self.created_by = created_by
        self.updated_by = updated_by
        self.created_at = created_at
        self.updated_at = updated_at
