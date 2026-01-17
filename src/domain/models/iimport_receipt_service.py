from abc import ABC, abstractmethod
from domain.models.import_receipt import ImportReceipt
from typing import List, Optional
from datetime import date

class IImportReceiptService(ABC):
    @abstractmethod
    def create_import_receipt_with_details(self, warehouse_id: int, invoice_id: int = None,
                                           import_date: date = None, details: List[dict] = None) -> ImportReceipt:
        pass

    @abstractmethod
    def get_import_receipt(self, import_receipt_id: int, household_id: int) -> Optional[ImportReceipt]:
        pass

    @abstractmethod
    def list_import_receipts(self, household_id: int) -> List[ImportReceipt]:
        pass

    @abstractmethod
    def update_import_receipt(self, import_receipt_id: int, household_id: int,
                              warehouse_id: int = None, import_date: date = None) -> ImportReceipt:
        pass
