from abc import ABC, abstractmethod
from domain.models.unit import Unit
from typing import List, Optional
from datetime import datetime

class IUnitService(ABC):
    @abstractmethod
    def create_unit(self, household_id: int, name: str, description: str = None, status: str = None) -> Unit:
        pass

    @abstractmethod
    def get_unit(self, unit_id: int, household_id: int) -> Optional[Unit]:
        pass

    @abstractmethod
    def list_units(self, household_id: int) -> List[Unit]:
        pass

    @abstractmethod
    def update_unit(self, unit_id: int, household_id: int, name: str = None, description: str = None, status: str = None) -> Unit:
        pass

    @abstractmethod
    def delete_unit(self, unit_id: int, household_id: int) -> None:
        pass
