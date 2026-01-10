from dataclasses import dataclass
from typing import Optional


@dataclass
class Inventory:
    id: Optional[int]
    product_id: int
    quantity_in_stock: int