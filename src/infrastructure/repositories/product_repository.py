from domain.models.iproduct_repository import IProductRepository
from domain.models.product import Product
from typing import List, Optional
from infrastructure.models import Product as ProductModel
from infrastructure.databases.mssql import session

class ProductRepository(IProductRepository):
    def __init__(self, session=session):
        self.session = session
    def add(self, product: Product) -> ProductModel:
        try:
            product_model = ProductModel(
                household_id=product.household_id,
                category_id=product.category_id,
                name=product.name,
                image_url=product.image_url,
                description=product.description,
                status=product.status,
                created_at=product.created_at,
                updated_at=product.updated_at
            )
            self.session.add(product_model)
            self.session.commit()
            self.session.refresh(product_model)
            return product_model
        except Exception as e:
            self.session.rollback() 
            raise ValueError(f'Error creating product: {str(e)}')
        
    def get_by_id(self, product_id: int, household_id: int) -> Optional[ProductModel]:
        return self.session.query(ProductModel).filter_by(id=product_id, household_id=household_id).first()
        
    def list(self, household_id: int) -> List[ProductModel]:
        return self.session.query(ProductModel).filter_by(household_id=household_id).all()
        
    def update(self, product: Product) -> ProductModel:
        try:
            product_model = self.session.query(ProductModel).filter_by(id=product.id, household_id=product.household_id).first()
            if not product_model:
                raise ValueError('Product not found')
                
            if product.category_id is not None:
                product_model.category_id = product.category_id
            if product.name is not None:
                product_model.name = product.name
            if product.image_url is not None:
                product_model.image_url = product.image_url    
            if product.description is not None:
                product_model.description = product.description
            if product.status is not None:
                product_model.status = product.status
            if product.updated_at is not None:
                product_model.updated_at = product.updated_at
                
            self.session.commit()
            self.session.refresh(product_model)
            return product_model
        except Exception as e: 
            self.session.rollback()
            raise ValueError(f'Error updating product: {str(e)}')
            
    def delete(self, product_id: int, household_id: int) -> None:
        try:
            product = self.session.query(ProductModel).filter_by(id=product_id, household_id=household_id).first()
            if product:
                self.session.delete(product)
                self.session.commit()
            else:
                raise ValueError('Product not found')
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error deleting product: {str(e)}')