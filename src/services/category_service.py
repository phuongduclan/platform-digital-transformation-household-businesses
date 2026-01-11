from domain.models.category import Category
from domain.models.icategory_repository import ICategoryRepository
from typing import List, Optional
from datetime import datetime

class CategoryService:
    def __init__(self, repository: ICategoryRepository):
        self.repository = repository

    def create_category(self, household_id:int, name: str, description: str = None, 
                        status: str = None) -> Category:
        now = datetime.utcnow()
        category = Category(household_id=household_id, name=name, description=description,
                           status=status, created_at=now, updated_at=now)
        return self.repository.add(category)

    def get_category(self, category_id: int, household_id: int) -> Optional[Category]:
        return self.repository.get_by_id(category_id, household_id)

    def list_categories(self, household_id: int) -> List[Category]:
        return self.repository.list(household_id)

    def update_category(self, category_id: int, household_id: int, name: str = None, description: str = None,
                        status: str = None) -> Category:
        now = datetime.utcnow()
        category = Category(id=category_id, household_id=household_id, name=name, description=description,
                           status=status, updated_at=now)
        return self.repository.update(category)

    def delete_category(self, category_id: int, household_id: int) -> None:
        self.repository.delete(category_id, household_id)