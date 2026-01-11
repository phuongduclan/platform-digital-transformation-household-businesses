from datetime import datetime
from typing import Optional

class PaymentMethod:
    def __init__(self, id: int = None, name: str = None, status: str = None,
                 created_at: datetime = None, updated_at: datetime = None):
        self.id = id
        self.name = name
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
