from abc import ABC, abstractmethod
from .accounting_ledger import AccountingLedger
from typing import List, Optional
from datetime import datetime

class IAccountingLedgerRepository(ABC):
    @abstractmethod
    def create(self, accounting_ledger: AccountingLedger) -> AccountingLedger:
        pass

    @abstractmethod
    def get_by_id(self, accounting_ledger_id: int, household_id: int = None) -> Optional[AccountingLedger]:
        pass

    @abstractmethod
    def list(self, household_id: int, from_date: datetime = None, to_date: datetime = None,
             movement_type: str = None) -> List[AccountingLedger]:
        pass

    @abstractmethod
    def get_by_invoice_id(self, invoice_id: int, household_id: int = None) -> Optional[AccountingLedger]:
        """Lấy accounting ledger theo invoice_id"""
        pass
