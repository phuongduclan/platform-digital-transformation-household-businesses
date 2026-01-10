from abc import ABC, abstractmethod
from typing import List, Optional
from .import_receipt import ImportReceipt


class IImportReceiptRepository(ABC):

    @abstractmethod
    def get_by_id(self, receipt_id: int) -> Optional[ImportReceipt]:
        pass

    @abstractmethod
    def get_all(self) -> List[ImportReceipt]:
        pass

    @abstractmethod
    def add(self, receipt: ImportReceipt) -> None:
        pass

