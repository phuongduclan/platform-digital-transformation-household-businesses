from abc import ABC, abstractmethod
from domain.models.payment import Payment
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

class IPaymentService(ABC):
    @abstractmethod
    def create_payment(self, invoice_id: int, method_id: int, amount: Decimal,
                      description: str = None, created_by: str = None,
                      household_id: int = None) -> Payment:
        pass

    @abstractmethod
    def get_payment(self, payment_id: int, household_id: int) -> Optional[Payment]:
        pass

    @abstractmethod
    def list_payments(self, household_id: int, invoice_id: int = None, customer_id: int = None) -> List[Payment]:
        pass

    @abstractmethod
    def update_payment(self, payment_id: int, household_id: int, method_id: int = None,
                      amount: Decimal = None, description: str = None) -> Payment:
        pass

    @abstractmethod
    def delete_payment(self, payment_id: int, household_id: int) -> None:
        pass
