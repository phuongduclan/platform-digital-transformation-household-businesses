from domain.models.warehouse import Warehouse
from domain.models.iwarehouse_repository import IWarehouseRepository
from typing import List, Optional
from datetime import datetime


class WarehouseService:
    def __init__(self, repository: IWarehouseRepository):
        self.repository = repository

    def create_warehouse(self, household_id: int, name: str,
                         address: str, description: str = None, status: str = None) -> Warehouse:
        now = datetime.utcnow()
        warehouse = Warehouse(
            household_id=household_id,
            name=name,
            address=address,
            description=description,
            status=status,
            created_at=now,
            updated_at=now
        )
        return self.repository.add(warehouse)

    def get_warehouse(self, warehouse_id: int, household_id: int) -> Optional[Warehouse]:
        return self.repository.get_by_id(warehouse_id, household_id)

    def list_warehouses(self, household_id: int) -> List[Warehouse]:
        return self.repository.list(household_id)

    def update_warehouse(
        self,
        warehouse_id: int,
        household_id: int,
        name: str = None,
        address: str = None,
        description: str = None,
        status: str = None
    ) -> Warehouse:
        now = datetime.utcnow()
        warehouse = Warehouse(
            id=warehouse_id,
            household_id=household_id,
            name=name,
            address=address,
            description=description,
            status=status,
            updated_at=now
        )
        return self.repository.update(warehouse)

    def delete_warehouse(self, warehouse_id: int, household_id: int) -> None:
        self.repository.delete(warehouse_id, household_id)
