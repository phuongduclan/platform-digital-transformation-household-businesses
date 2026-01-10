from dataclasses import dataclass
from typing import Optional


@dataclass
class ImportDetail:
    id: Optional[int]
    import_receipt_id: int
    product_id: int
    quantity: int
    unit_price: float
