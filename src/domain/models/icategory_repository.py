from abc import ABC, abstractmethod
from .category import Category
from typing import List, Optional

class ICategoryRepository(ABC):
    @abstractmethod
    def add(self, category: Category) -> Category:
        pass

    @abstractmethod
    def get_by_id(self, category_id: int) -> Optional[Category]:
        pass

    @abstractmethod
    def list(self) -> List[Category]:
        pass

    @abstractmethod
    def update(self, category: Category) -> Category:
        pass

    @abstractmethod
    def delete(self, category_id: int) -> None:
        pass