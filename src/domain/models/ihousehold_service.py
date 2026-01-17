from abc import ABC, abstractmethod
from domain.models.household import Household
from typing import List, Optional
from datetime import datetime

class IHouseholdService(ABC):
    @abstractmethod
    def create_household(
        self,
        tax_code: Optional[str] = None,
        name: Optional[str] = None,
        phone: Optional[str] = None,
        address: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        created_by: Optional[str] = None,
        updated_by: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> Household:
        pass

    @abstractmethod
    def get_household(self, household_id: int) -> Optional[Household]:
        pass

    @abstractmethod
    def list_households(self) -> List[Household]:
        pass

    @abstractmethod
    def get_own_household(self, household_id: int) -> Optional[Household]:
        pass

    @abstractmethod
    def update_own_household(
        self,
        household_id: int,
        tax_code: Optional[str] = None,
        name: Optional[str] = None,
        phone: Optional[str] = None,
        address: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        updated_by: Optional[str] = None,
        updated_at: Optional[datetime] = None,
    ) -> Household:
        pass

    @abstractmethod
    def update_household(
        self,
        household_id: int,
        tax_code: Optional[str] = None,
        name: Optional[str] = None,
        phone: Optional[str] = None,
        address: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        created_by: Optional[str] = None,
        updated_by: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> Household:
        pass

    @abstractmethod
    def delete_household(self, household_id: int) -> None:
        pass
