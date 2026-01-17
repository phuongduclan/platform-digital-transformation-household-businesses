from abc import ABC, abstractmethod
from domain.models.customer import Customer
from typing import List, Optional, Dict

class ICustomerService(ABC):
    @abstractmethod
    def create_customer(self, household_id: int, tax_code: str = None, name: str = None,
                      phone: str = None, address: str = None, description: str = None,
                      status: str = 'Active', created_by: str = None) -> Customer:
        pass

    @abstractmethod
    def get_customer(self, customer_id: int, household_id: int) -> Optional[Customer]:
        pass

    @abstractmethod
    def list_customers(self, household_id: int, status: str = None) -> List[Customer]:
        pass

    @abstractmethod
    def update_customer(self, customer_id: int, household_id: int, tax_code: str = None,
                       name: str = None, phone: str = None, address: str = None,
                       description: str = None, status: str = None,
                       updated_by: str = None) -> Customer:
        pass

    @abstractmethod
    def delete_customer(self, customer_id: int, household_id: int) -> None:
        pass

    @abstractmethod
    def get_customer_purchase_history(self, customer_id: int, household_id: int) -> List[dict]:
        pass

    @abstractmethod
    def get_customer_debt(self, customer_id: int, household_id: int) -> dict:
        pass
