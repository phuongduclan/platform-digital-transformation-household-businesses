from abc import ABC, abstractmethod
from .customer import Customer
from typing import List, Optional

class ICustomerRepository(ABC):
    @abstractmethod
    def create(self, customer: Customer) -> Customer:
        pass

    @abstractmethod
    def get_by_id(self, customer_id: int, household_id: int = None) -> Optional[Customer]:
        pass

    @abstractmethod
    def list(self, household_id: int, status: str = None) -> List[Customer]:
        pass

    @abstractmethod
    def update(self, customer: Customer) -> Customer:
        pass

    @abstractmethod
    def delete(self, customer_id: int, household_id: int = None) -> None:
        pass
