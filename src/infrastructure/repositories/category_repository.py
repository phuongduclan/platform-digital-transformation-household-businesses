from domain.models.category import Category
from domain.models.icategory_repository import ICategoryRepository
from typing import List, Optional
from infrastructure.models import Category as CategoryModel
from infrastructure.databases.mssql import session

class CategoryRepository(ICategoryRepository):
    def __init__(self, session=session):
        self.session = session

    def add(self, category: Category) -> CategoryModel:
        try:
            category_model = CategoryModel(
                household_id=category.household_id,
                name=category.name,
                description=category.description,
                status=category.status,
                created_at=category.created_at,
                updated_at=category.updated_at
            )
            self.session.add(category_model)
            self.session.commit()
            self.session.refresh(category_model)
            return category_model
        except Exception as e:
            self.session.rollback() 
            raise ValueError(f'Error creating category: {str(e)}')

    def get_by_id(self, category_id: int, household_id: int) -> Optional[CategoryModel]:
        return self.session.query(CategoryModel).filter_by(id=category_id, household_id=household_id).first()

    def list(self, household_id: int) -> List[CategoryModel]:
        return self.session.query(CategoryModel).filter_by(household_id=household_id).all()
    
    def update(self, category: Category) -> CategoryModel:
        try:
            category_model = self.session.query(CategoryModel).filter_by(id=category.id, household_id=category.household_id).first()
            if not category_model:
                raise ValueError('Category not found')
            
            if category.name is not None:
                category_model.name = category.name
            if category.description is not None:
                category_model.description = category.description
            if category.status is not None:
                category_model.status = category.status
            if category.updated_at is not None:
                category_model.updated_at = category.updated_at
            
            self.session.commit()
            self.session.refresh(category_model)
            return category_model
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error updating category: {str(e)}')
        
    def delete(self, category_id: int, household_id: int) -> None:
        try:
            category_model = self.session.query(CategoryModel).filter_by(id=category_id, household_id=household_id).first()
            if not category_model:
                raise ValueError('Category not found')
            self.session.delete(category_model)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error deleting category: {str(e)}')