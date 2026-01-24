from domain.models.iinventory_repository import IInventoryRepository
from domain.models.inventory import Inventory
from typing import List, Optional
from infrastructure.models.inventory_model import Inventory as InventoryModel
from infrastructure.models.warehouse_model import Warehouse
from infrastructure.databases.mssql import session
from datetime import datetime
from infrastructure.utils.datetime_utils import vietnam_now

class InventoryRepository(IInventoryRepository):
    def __init__(self, session=session):
        self.session = session

    def get_by_product_and_warehouse(self, product_id: int, warehouse_id: int, household_id: int = None) -> Optional[Inventory]:
        query = self.session.query(InventoryModel).join(Warehouse).filter(
            InventoryModel.product_id == product_id,
            InventoryModel.warehouse_id == warehouse_id
        )
        if household_id is not None:
            query = query.filter(Warehouse.household_id == household_id)
        inventory_model = query.first()
        return self._to_domain(inventory_model) if inventory_model else None

    def get_by_product_unit_and_warehouse(self, product_id: int, unit_id: int, warehouse_id: int, household_id: int = None) -> Optional[Inventory]:
        """Lấy inventory theo product_id, unit_id và warehouse_id"""
        query = self.session.query(InventoryModel).join(Warehouse).filter(
            InventoryModel.product_id == product_id,
            InventoryModel.unit_id == unit_id,
            InventoryModel.warehouse_id == warehouse_id
        )
        if household_id is not None:
            query = query.filter(Warehouse.household_id == household_id)
        inventory_model = query.first()
        return self._to_domain(inventory_model) if inventory_model else None

    def list(self, household_id: int, warehouse_id: int = None, product_id: int = None) -> List[Inventory]:
        query = self.session.query(InventoryModel).join(Warehouse).filter(Warehouse.household_id == household_id)
        if warehouse_id is not None:
            query = query.filter(InventoryModel.warehouse_id == warehouse_id)
        if product_id is not None:
            query = query.filter(InventoryModel.product_id == product_id)
        inventory_models = query.all()
        return [self._to_domain(im) for im in inventory_models]

    def create_or_update(self, inventory: Inventory) -> Inventory:
        try:
            existing = self.get_by_product_and_warehouse(
                inventory.product_id, inventory.warehouse_id
            )
            if existing:
                existing.quantity = inventory.quantity
                existing.updated_at = vietnam_now()
                return self.update(existing)
            else:
                inventory_model = InventoryModel(
                    product_id=inventory.product_id,
                    unit_id=inventory.unit_id,
                    warehouse_id=inventory.warehouse_id,
                    quantity=inventory.quantity,
                    created_at=vietnam_now(),
                    updated_at=vietnam_now()
                )
                self.session.add(inventory_model)
                self.session.flush()
                self.session.refresh(inventory_model)
                return self._to_domain(inventory_model)
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error creating/updating inventory: {str(e)}')

    def increase_quantity(self, product_id: int, unit_id: int, warehouse_id: int, quantity: int, household_id: int = None) -> Inventory:
        """Tăng quantity (tạo mới nếu chưa có, cộng thêm nếu đã có)"""
        try:
            existing = self.get_by_product_unit_and_warehouse(product_id, unit_id, warehouse_id, household_id)
            if existing:
                existing.quantity += quantity
                existing.updated_at = vietnam_now()
                return self.update(existing)
            else:
                inventory = Inventory(
                    id=None,
                    product_id=product_id,
                    unit_id=unit_id,
                    warehouse_id=warehouse_id,
                    quantity=quantity,
                    created_at=vietnam_now(),
                    updated_at=vietnam_now()
                )
                return self.create_or_update(inventory)
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error increasing inventory quantity: {str(e)}')

    def decrease_quantity(self, product_id: int, unit_id: int, warehouse_id: int, quantity: int, household_id: int = None) -> Inventory:
        """Giảm quantity (kiểm tra đủ số lượng trước)"""
        try:
            existing = self.get_by_product_unit_and_warehouse(product_id, unit_id, warehouse_id, household_id)
            if not existing:
                raise ValueError(f'Inventory not found for product_id={product_id}, warehouse_id={warehouse_id}')
            if existing.quantity < quantity:
                raise ValueError(f'Insufficient inventory. Available: {existing.quantity}, Required: {quantity}')
            
            existing.quantity -= quantity
            existing.updated_at = vietnam_now()
            return self.update(existing)
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error decreasing inventory quantity: {str(e)}')

    def update(self, inventory: Inventory, household_id: int = None) -> Inventory:
        try:
            query = self.session.query(InventoryModel).filter_by(id=inventory.id)
            if household_id is not None:
                query = query.join(Warehouse).filter(Warehouse.household_id == household_id)
            inventory_model = query.first()
            if not inventory_model:
                raise ValueError('Inventory not found')

            if inventory.quantity is not None:
                inventory_model.quantity = inventory.quantity
            if inventory.updated_at is not None:
                inventory_model.updated_at = inventory.updated_at

            self.session.flush()
            self.session.refresh(inventory_model)
            return self._to_domain(inventory_model)
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error updating inventory: {str(e)}')

    def _to_domain(self, inventory_model: InventoryModel) -> Inventory:
        return Inventory(
            id=inventory_model.id,
            product_id=inventory_model.product_id,
            unit_id=inventory_model.unit_id,
            warehouse_id=inventory_model.warehouse_id,
            quantity=inventory_model.quantity,
            created_at=inventory_model.created_at,
            updated_at=inventory_model.updated_at
        )
