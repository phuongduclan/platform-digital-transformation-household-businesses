from abc import ABC, abstractmethod
from domain.models.inventory import Inventory
from typing import List, Optional

class IInventoryRepository(ABC):
    @abstractmethod
    def get_by_product_and_warehouse(self, product_id: int, warehouse_id: int, household_id: int = None) -> Optional[Inventory]:
        pass

    @abstractmethod
    def get_by_product_unit_and_warehouse(self, product_id: int, unit_id: int, warehouse_id: int, household_id: int = None) -> Optional[Inventory]:
        """Lấy inventory theo product_id, unit_id và warehouse_id"""
        pass

    @abstractmethod
    def list(self, household_id: int, warehouse_id: int = None, product_id: int = None) -> List[Inventory]:
        pass

    @abstractmethod
    def create_or_update(self, inventory: Inventory) -> Inventory:
        """Tạo mới nếu chưa có, hoặc cập nhật nếu đã có"""
        pass

    @abstractmethod
    def increase_quantity(self, product_id: int, unit_id: int, warehouse_id: int, quantity: int, household_id: int = None) -> Inventory:
        """Tăng quantity (tạo mới nếu chưa có, cộng thêm nếu đã có)"""
        pass

    @abstractmethod
    def decrease_quantity(self, product_id: int, unit_id: int, warehouse_id: int, quantity: int, household_id: int = None) -> Inventory:
        """Giảm quantity (kiểm tra đủ số lượng trước)"""
        pass

    @abstractmethod
    def update(self, inventory: Inventory, household_id: int = None) -> Inventory:
        pass
