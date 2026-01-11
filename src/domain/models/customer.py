from datetime import datetime
from typing import Optional

class Customer:
    def __init__(self, id: int = None, household_id: int = None, tax_code: str = None,
                 name: str = None, phone: str = None, address: str = None,
                 description: str = None, status: str = None,
                 created_by: str = None, updated_by: str = None,
                 created_at: datetime = None, updated_at: datetime = None):
        self.id = id
        self.household_id = household_id
        self.tax_code = tax_code
        self.name = name
        self.phone = phone
        self.address = address
        self.description = description
        self.status = status
        self.created_by = created_by
        self.updated_by = updated_by
        self.created_at = created_at
        self.updated_at = updated_at
