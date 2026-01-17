from abc import ABC, abstractmethod
from domain.models.accounting_ledger import AccountingLedger
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

class IAccountingLedgerService(ABC):
    @abstractmethod
    def get_accounting_ledger(self, accounting_ledger_id: int, household_id: int) -> Optional[AccountingLedger]:
        pass

    @abstractmethod
    def list_accounting_ledgers(self, household_id: int, from_date: datetime = None,
                               to_date: datetime = None, movement_type: str = None) -> List[AccountingLedger]:
        pass

    @abstractmethod
    def get_by_invoice_id(self, invoice_id: int, household_id: int) -> Optional[AccountingLedger]:
        pass

    @abstractmethod
    def create_accounting_ledger(self, invoice_id: int, transaction_date: datetime,
                                 debit_amount: Decimal = None, credit_amount: Decimal = None,
                                 description: str = None, movement_type: str = None,
                                 household_id: int = None) -> AccountingLedger:
        pass
