from abc import ABC, abstractmethod
from .warehouse import Warehouse
from typing import List, Optional

class IWarehouseRepository(ABC):
    @abstractmethod
    def add(self, warehouse: Warehouse) -> Warehouse:
        pass
    
    @abstractmethod
    def get_by_id(self, warehouse_id: int, household_id: int) -> Optional[Warehouse]:
        pass

    @abstractmethod
    def list(self, household_id: int) -> List[Warehouse]:
        pass

    @abstractmethod
    def update(self, warehouse: Warehouse) -> Warehouse:
        pass

    @abstractmethod
    def delete(self, warehouse_id: int, household_id: int) -> None:
        pass
