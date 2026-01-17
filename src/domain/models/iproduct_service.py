from abc import ABC, abstractmethod
from domain.models.product import Product
from typing import List, Optional
from datetime import datetime

class IProductService(ABC):
    @abstractmethod
    def create_product(self, household_id: int, category_id: int, name: str,
                       image_url: str, description: str, status: str,
                       created_at: datetime = None, updated_at: datetime = None) -> Product:
        pass

    @abstractmethod
    def get_product(self, product_id: int, household_id: int) -> Optional[Product]:
        pass

    @abstractmethod
    def list_products(self, household_id: int) -> List[Product]:
        pass

    @abstractmethod
    def update_product(self, product_id: int, household_id: int, category_id: int = None,
                       name: str = None, image_url: str = None, description: str = None,
                       status: str = None, updated_at: datetime = None) -> Product:
        pass

    @abstractmethod
    def delete_product(self, product_id: int, household_id: int) -> None:
        pass
