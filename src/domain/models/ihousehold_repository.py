from abc import ABC, abstractmethod
from .household import Household
from typing import List, Optional

class IHouseholdRepository(ABC):
    @abstractmethod
    def add(self, household: Household) -> Household:
        pass

    @abstractmethod
    def get_by_id(self, household_id: int) -> Optional[Household]:
        pass

    @abstractmethod
    def list(self) -> List[Household]:
        pass

    @abstractmethod
    def update(self, household: Household) -> Household:
        pass

    @abstractmethod
    def delete(self, household_id: int) -> None:
        pass
