from datetime import datetime
from decimal import Decimal
from typing import Optional

class Payment:
    def __init__(self, id: int = None, invoice_id: int = None, method_id: int = None,
                 amount: Decimal = None, description: str = None, status: str = None,
                 created_by: str = None, updated_by: str = None,
                 created_at: datetime = None, updated_at: datetime = None):
        self.id = id
        self.invoice_id = invoice_id
        self.method_id = method_id
        self.amount = amount
        self.description = description
        self.status = status
        self.created_by = created_by
        self.updated_by = updated_by
        self.created_at = created_at
        self.updated_at = updated_at
