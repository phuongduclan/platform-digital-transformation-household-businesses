from domain.models.product import Product
from domain.models.iproduct_repository import IProductRepository
from typing import List, Optional
from datetime import datetime

class ProductService:
    def __init__(self, repository: IProductRepository):
        self.repository = repository

    def create_product(self, household_id: int, category_id: int, name: str,
                       image_url: str, description: str, status: str,
                       created_at: datetime = None, updated_at: datetime = None) -> Product:
        now = datetime.utcnow()
        product = Product(id=None, household_id=household_id, category_id=category_id,
                          name=name, image_url=image_url, description=description,
                          status=status, created_at=created_at or now, updated_at=updated_at or now)
        return self.repository.add(product)
    
    def get_product(self, product_id: int, household_id: int) -> Optional[Product]:
        return self.repository.get_by_id(product_id, household_id)
    
    def list_products(self, household_id: int) -> List[Product]:
        return self.repository.list(household_id)
    
    def update_product(self, product_id: int, household_id: int, category_id: int = None,
                       name: str = None, image_url: str = None, description: str = None,
                       status: str = None, updated_at: datetime = None) -> Product:
        now = datetime.utcnow()
        product = Product(id=product_id, household_id=household_id, category_id=category_id,
                          name=name, image_url=image_url, description=description,
                          status=status, updated_at=updated_at or now)
        return self.repository.update(product)

    def delete_product(self, product_id: int, household_id: int) -> None:
        self.repository.delete(product_id, household_id)
    