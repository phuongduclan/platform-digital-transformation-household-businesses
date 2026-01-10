from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ImportReceipt:
    id: Optional[int]
    receipt_code: str
    supplier_name: str
    import_date: datetime
    total_amount: float
    note: Optional[str] = None
