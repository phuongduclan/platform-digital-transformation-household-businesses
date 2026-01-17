from abc import ABC, abstractmethod
from domain.models.payment_method import PaymentMethod
from typing import List, Optional

class IPaymentMethodService(ABC):
    @abstractmethod
    def list_payment_methods(self, status: str = 'Active') -> List[PaymentMethod]:
        """List payment methods (Owner chỉ xem, Admin quản lý)"""
        pass

    @abstractmethod
    def get_payment_method(self, payment_method_id: int) -> Optional[PaymentMethod]:
        pass

    @abstractmethod
    def create_payment_method(self, name: str, status: str = 'Active') -> PaymentMethod:
        """Admin only: Create payment method"""
        pass

    @abstractmethod
    def update_payment_method(self, payment_method_id: int, name: str = None, status: str = None) -> PaymentMethod:
        """Admin only: Update payment method"""
        pass

    @abstractmethod
    def delete_payment_method(self, payment_method_id: int) -> None:
        """Admin only: Delete payment method"""
        pass
