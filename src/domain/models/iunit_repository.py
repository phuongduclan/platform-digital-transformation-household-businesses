from abc import ABC, abstractmethod
from .unit import Unit
from typing import List, Optional

class IUnitRepository(ABC):
    @abstractmethod
    def add(self, unit: Unit) -> Unit:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[Unit]:
        pass

    @abstractmethod
    def list(self) -> List[Unit]:
        pass

    @abstractmethod
    def update(self, unit: Unit) -> Unit:
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        pass