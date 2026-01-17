from abc import ABC, abstractmethod
from domain.models.inventory import Inventory
from typing import List, Optional

class IInventoryService(ABC):
    @abstractmethod
    def get_inventory(self, product_id: int, warehouse_id: int, household_id: int, unit_id: int = None) -> Optional[Inventory]:
        pass

    @abstractmethod
    def list_inventory(self, household_id: int, warehouse_id: int = None, product_id: int = None, unit_id: int = None) -> List[Inventory]:
        pass

    @abstractmethod
    def increase_inventory(self, product_id: int, unit_id: int, warehouse_id: int,
                          quantity: int, household_id: int) -> Inventory:
        pass

    @abstractmethod
    def decrease_inventory(self, product_id: int, unit_id: int, warehouse_id: int,
                          quantity: int, household_id: int) -> Inventory:
        pass

    @abstractmethod
    def update_inventory(self, inventory_id: int, quantity: int, household_id: int) -> Inventory:
        pass
