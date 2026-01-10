from dataclasses import dataclass
from typing import Optional


@dataclass
class ExportDetail:
    id: Optional[int]
    export_receipt_id: int
    product_id: int
    quantity: int
    unit_price: float
