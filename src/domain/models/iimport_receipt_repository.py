from abc import ABC, abstractmethod
from domain.models.import_receipt import ImportReceipt
from typing import List, Optional

class IImportReceiptRepository(ABC):
    @abstractmethod
    def create(self, import_receipt: ImportReceipt) -> ImportReceipt:
        pass

    @abstractmethod
    def get_by_id(self, import_receipt_id: int, household_id: int = None) -> Optional[ImportReceipt]:
        pass

    @abstractmethod
    def list(self, household_id: int) -> List[ImportReceipt]:
        pass

    @abstractmethod
    def update(self, import_receipt: ImportReceipt) -> ImportReceipt:
        pass
