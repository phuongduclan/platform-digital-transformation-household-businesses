from abc import ABC, abstractmethod
from .payment import Payment
from typing import List, Optional

class IPaymentRepository(ABC):
    @abstractmethod
    def create(self, payment: Payment) -> Payment:
        pass

    @abstractmethod
    def get_by_id(self, payment_id: int, household_id: int = None) -> Optional[Payment]:
        pass

    @abstractmethod
    def list(self, household_id: int, invoice_id: int = None, customer_id: int = None) -> List[Payment]:
        pass

    @abstractmethod
    def update(self, payment: Payment, household_id: int = None) -> Payment:
        pass

    @abstractmethod
    def delete(self, payment_id: int, household_id: int = None) -> None:
        pass
