from abc import ABC, abstractmethod
from .seller import Seller
from typing import List, Optional

class ISellerRepository(ABC):
    @abstractmethod
    def create(self, seller: Seller) -> Seller:
        pass

    @abstractmethod
    def get_by_id(self, seller_id: int, household_id: int = None) -> Optional[Seller]:
        pass

    @abstractmethod
    def list(self, household_id: int, status: str = None) -> List[Seller]:
        pass

    @abstractmethod
    def update(self, seller: Seller) -> Seller:
        pass

    @abstractmethod
    def delete(self, seller_id: int, household_id: int = None) -> None:
        pass
