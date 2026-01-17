from abc import ABC, abstractmethod
from domain.models.category import Category
from typing import List, Optional
from datetime import datetime

class ICategoryService(ABC):
    @abstractmethod
    def create_category(self, household_id: int, name: str, description: str = None, 
                        status: str = None) -> Category:
        pass

    @abstractmethod
    def get_category(self, category_id: int, household_id: int) -> Optional[Category]:
        pass

    @abstractmethod
    def list_categories(self, household_id: int) -> List[Category]:
        pass

    @abstractmethod
    def update_category(self, category_id: int, household_id: int, name: str = None, description: str = None,
                        status: str = None) -> Category:
        pass

    @abstractmethod
    def delete_category(self, category_id: int, household_id: int) -> None:
        pass
