from abc import ABC, abstractmethod
from .payment_method import PaymentMethod
from typing import List, Optional

class IPaymentMethodRepository(ABC):
    @abstractmethod
    def create(self, payment_method: PaymentMethod) -> PaymentMethod:
        pass

    @abstractmethod
    def get_by_id(self, payment_method_id: int) -> Optional[PaymentMethod]:
        pass

    @abstractmethod
    def list(self, status: str = 'Active') -> List[PaymentMethod]:
        pass

    @abstractmethod
    def update(self, payment_method: PaymentMethod) -> PaymentMethod:
        pass

    @abstractmethod
    def delete(self, payment_method_id: int) -> None:
        pass
