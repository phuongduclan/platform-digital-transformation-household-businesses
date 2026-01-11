from typing import Optional

class ImportDetail:
    def __init__(self, id: int = None, import_id: int = None, product_id: int = None,
                 unit_id: int = None, quantity: int = None):
        self.id = id
        self.import_id = import_id
        self.product_id = product_id
        self.unit_id = unit_id
        self.quantity = quantity
