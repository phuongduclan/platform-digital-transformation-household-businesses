from abc import ABC, abstractmethod
from domain.models.warehouse import Warehouse
from typing import List, Optional

class IWarehouseService(ABC):
    @abstractmethod
    def create_warehouse(self, household_id: int, name: str,
                         address: str, description: str = None, status: str = None) -> Warehouse:
        pass

    @abstractmethod
    def get_warehouse(self, warehouse_id: int, household_id: int) -> Optional[Warehouse]:
        pass

    @abstractmethod
    def list_warehouses(self, household_id: int) -> List[Warehouse]:
        pass

    @abstractmethod
    def update_warehouse(
        self,
        warehouse_id: int,
        household_id: int,
        name: str = None,
        address: str = None,
        description: str = None,
        status: str = None
    ) -> Warehouse:
        pass

    @abstractmethod
    def delete_warehouse(self, warehouse_id: int, household_id: int) -> None:
        pass
