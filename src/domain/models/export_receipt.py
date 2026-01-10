from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class ExportReceipt:
    id: Optional[int]
    receipt_code: str
    customer_name: str
    export_date: datetime
    total_amount: float
    note: Optional[str] = None
