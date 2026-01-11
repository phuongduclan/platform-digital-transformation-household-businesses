from typing import Optional
from datetime import datetime

class Household:
    def __init__(self,
                 id: Optional[int] = None,
                 tax_code: Optional[str] = None,
                 name: Optional[str] = None,
                 phone: Optional[str] = None,
                 address: Optional[str] = None,
                 description: Optional[str] = None,
                 status: Optional[str] = None,
                 created_by: Optional[str] = None,
                 updated_by: Optional[str] = None,
                 created_at: Optional[datetime] = None,
                 updated_at: Optional[datetime] = None):
        self.id = id
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
