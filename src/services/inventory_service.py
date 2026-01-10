from domain.models.iinventory_repository import IInventoryRepository

class InventoryService:

    def __init__(self, repo: IInventoryRepository):
        self.repo = repo

    def get_all(self, household_id: int):
        return self.repo.get_all(household_id)

    def get_by_product_warehouse(self, product_id: int, warehouse_id: int):
        return self.repo.get_by_product_warehouse(product_id, warehouse_id)
