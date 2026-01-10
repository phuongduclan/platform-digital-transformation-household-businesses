from abc import ABC, abstractmethod
from typing import List, Optional
from .export_receipt import ExportReceipt


class IExportReceiptRepository(ABC):

    @abstractmethod
    def get_by_id(self, receipt_id: int) -> Optional[ExportReceipt]:
        pass

    @abstractmethod
    def get_all(self) -> List[ExportReceipt]:
        pass

    @abstractmethod
    def add(self, receipt: ExportReceipt) -> None:
        pass
