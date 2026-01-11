from domain.models.warehouse import Warehouse
from domain.models.iwarehouse_repository import IWarehouseRepository
from typing import List, Optional
from infrastructure.models import Warehouse as WarehouseModel
from infrastructure.databases.mssql import session


class WarehouseRepository(IWarehouseRepository):
    def __init__(self, session=session):
        self.session = session

    def add(self, warehouse: Warehouse) -> WarehouseModel:
        try:
            warehouse_model = WarehouseModel(
                household_id=warehouse.household_id,
                name=warehouse.name,
                address=warehouse.address,
                description=warehouse.description,
                status=warehouse.status,
                created_at=warehouse.created_at,
                updated_at=warehouse.updated_at
            )
            self.session.add(warehouse_model)
            self.session.commit()
            self.session.refresh(warehouse_model)
            return warehouse_model
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Error creating warehouse: {str(e)}")

    def get_by_id(self, warehouse_id: int, household_id: int) -> Optional[WarehouseModel]:
        return self.session.query(WarehouseModel).filter_by(
            id=warehouse_id,
            household_id=household_id
        ).first()

    def list(self, household_id: int) -> List[WarehouseModel]:
        return self.session.query(WarehouseModel).filter_by(
            household_id=household_id
        ).all()

    def update(self, warehouse: Warehouse) -> WarehouseModel:
        try:
            warehouse_model = self.session.query(WarehouseModel).filter_by(
                id=warehouse.id,
                household_id=warehouse.household_id
            ).first()

            if not warehouse_model:
                raise ValueError("Warehouse not found")

            if warehouse.name is not None:
                warehouse_model.name = warehouse.name
            if warehouse.address is not None:
                warehouse_model.address = warehouse.address
            if warehouse.description is not None:
                warehouse_model.description = warehouse.description
            if warehouse.status is not None:
                warehouse_model.status = warehouse.status
            if warehouse.updated_at is not None:
                warehouse_model.updated_at = warehouse.updated_at

            self.session.commit()
            self.session.refresh(warehouse_model)
            return warehouse_model
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Error updating warehouse: {str(e)}")

    def delete(self, warehouse_id: int, household_id: int) -> None:
        try:
            warehouse_model = self.session.query(WarehouseModel).filter_by(
                id=warehouse_id,
                household_id=household_id
            ).first()

            if not warehouse_model:
                raise ValueError("Warehouse not found")

            self.session.delete(warehouse_model)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise ValueError(f"Error deleting warehouse: {str(e)}")
