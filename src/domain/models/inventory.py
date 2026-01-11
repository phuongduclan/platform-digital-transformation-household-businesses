from datetime import datetime
from typing import Optional

class Inventory:
    def __init__(self, id: int = None, product_id: int = None, unit_id: int = None,
                 warehouse_id: int = None, quantity: int = None,
                 created_at: datetime = None, updated_at: datetime = None):
        self.id = id
        self.product_id = product_id
        self.unit_id = unit_id
        self.warehouse_id = warehouse_id
        self.quantity = quantity
        self.created_at = created_at
        self.updated_at = updated_at
