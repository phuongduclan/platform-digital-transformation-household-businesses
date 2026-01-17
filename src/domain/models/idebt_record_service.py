from abc import ABC, abstractmethod
from domain.models.debt_record import DebtRecord
from typing import List, Optional
from decimal import Decimal

class IDebtRecordService(ABC):
    @abstractmethod
    def get_debt_record(self, debt_record_id: int, household_id: int) -> Optional[DebtRecord]:
        pass

    @abstractmethod
    def list_debt_records(self, household_id: int, customer_id: int = None) -> List[DebtRecord]:
        pass

    @abstractmethod
    def get_customer_debt_records(self, customer_id: int, household_id: int) -> List[DebtRecord]:
        pass

    @abstractmethod
    def get_customer_balance(self, customer_id: int, household_id: int) -> Decimal:
        pass

    @abstractmethod
    def create_debt_record(self, customer_id: int, invoice_id: int = None, payment_id: int = None,
                          debit_amount: Decimal = None, credit_amount: Decimal = None,
                          description: str = None, household_id: int = None) -> DebtRecord:
        pass
