from domain.models.inventory import Inventory
from domain.models.iinventory_repository import IInventoryRepository
from typing import List, Optional

class InventoryService:
    def __init__(self, repository: IInventoryRepository):
        self.repository = repository

    def get_inventory(self, product_id: int, warehouse_id: int, household_id: int, unit_id: int = None) -> Optional[Inventory]:
        """
        Lấy inventory theo product_id và warehouse_id.
        Nếu có unit_id, lấy chính xác theo product_id, unit_id và warehouse_id.
        """
        if unit_id is not None:
            return self.repository.get_by_product_unit_and_warehouse(product_id, unit_id, warehouse_id, household_id)
        return self.repository.get_by_product_and_warehouse(product_id, warehouse_id, household_id)

    def list_inventory(self, household_id: int, warehouse_id: int = None, product_id: int = None, unit_id: int = None) -> List[Inventory]:
        """List inventory với các filter tùy chọn"""
        inventory_list = self.repository.list(household_id, warehouse_id, product_id)
        if unit_id is not None:
            # Filter thêm theo unit_id nếu có
            inventory_list = [inv for inv in inventory_list if inv.unit_id == unit_id]
        return inventory_list

    def increase_inventory(self, product_id: int, unit_id: int, warehouse_id: int,
                          quantity: int, household_id: int) -> Inventory:
        """
        Tăng inventory quantity (tạo mới nếu chưa có, cộng thêm nếu đã có).
        Được gọi tự động khi ImportReceipt được tạo.
        """
        return self.repository.increase_quantity(product_id, unit_id, warehouse_id, quantity, household_id)

    def decrease_inventory(self, product_id: int, unit_id: int, warehouse_id: int,
                          quantity: int, household_id: int) -> Inventory:
        """
        Giảm inventory quantity (kiểm tra đủ số lượng trước).
        Được gọi tự động khi ExportReceipt được tạo.
        Nếu không đủ → trả lỗi.
        """
        return self.repository.decrease_quantity(product_id, unit_id, warehouse_id, quantity, household_id)

    def update_inventory(self, inventory_id: int, quantity: int, household_id: int) -> Inventory:
        """
        Owner chỉ được điều chỉnh quantity nếu cần.
        """
        # Lấy inventory từ id (cần thêm method get_by_id vào repository nếu cần)
        # Tạm thời dùng update trực tiếp
        inventory = Inventory(id=inventory_id, quantity=quantity)
        return self.repository.update(inventory)
