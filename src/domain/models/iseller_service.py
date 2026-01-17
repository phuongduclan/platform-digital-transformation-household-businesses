from abc import ABC, abstractmethod
from domain.models.seller import Seller
from typing import List, Optional

class ISellerService(ABC):
    @abstractmethod
    def create_seller(self, household_id: int, tax_code: str = None, name: str = None,
                     phone: str = None, address: str = None, description: str = None,
                     status: str = 'Active', created_by: str = None) -> Seller:
        pass

    @abstractmethod
    def get_seller(self, seller_id: int, household_id: int) -> Optional[Seller]:
        pass

    @abstractmethod
    def list_sellers(self, household_id: int, status: str = None) -> List[Seller]:
        pass

    @abstractmethod
    def update_seller(self, seller_id: int, household_id: int, tax_code: str = None,
                     name: str = None, phone: str = None, address: str = None,
                     description: str = None, status: str = None,
                     updated_by: str = None) -> Seller:
        pass

    @abstractmethod
    def delete_seller(self, seller_id: int, household_id: int) -> None:
        pass
