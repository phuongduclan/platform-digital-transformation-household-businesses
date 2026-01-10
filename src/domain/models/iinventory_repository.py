from abc import ABC, abstractmethod
from .inventory import InventoryDTO

class IInventoryRepository(ABC):

    @abstractmethod
    def get_all(self, household_id: int): pass

    @abstractmethod
    def get_by_product_warehouse(self, product_id: int, warehouse_id: int): pass

    @abstractmethod
    def create(self, dto: InventoryDTO): pass

    @abstractmethod
    def update(self, inventory_id: int, dto: InventoryDTO): pass

    @abstractmethod
    def delete(self, inventory_id: int): pass

    @abstractmethod
    def increase(self, product_id: int, warehouse_id: int, quantity: int): pass

    @abstractmethod
    def decrease(self, product_id: int, warehouse_id: int, quantity: int): pass
