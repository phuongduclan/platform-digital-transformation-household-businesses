from abc import ABC, abstractmethod
from .debt_record import DebtRecord
from typing import List, Optional

class IDebtRecordRepository(ABC):
    @abstractmethod
    def create(self, debt_record: DebtRecord) -> DebtRecord:
        pass

    @abstractmethod
    def get_by_id(self, debt_record_id: int, household_id: int = None) -> Optional[DebtRecord]:
        pass

    @abstractmethod
    def list(self, household_id: int, customer_id: int = None) -> List[DebtRecord]:
        pass

    @abstractmethod
    def get_by_customer_id(self, customer_id: int, household_id: int = None) -> List[DebtRecord]:
        """Lấy tất cả debt records của 1 customer"""
        pass

    @abstractmethod
    def get_customer_balance(self, customer_id: int, household_id: int = None) -> Optional[DebtRecord]:
        """Lấy balance hiện tại của customer (bản ghi mới nhất)"""
        pass
