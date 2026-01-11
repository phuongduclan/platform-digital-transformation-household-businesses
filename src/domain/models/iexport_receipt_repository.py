from abc import ABC, abstractmethod
from domain.models.export_receipt import ExportReceipt
from typing import List, Optional

class IExportReceiptRepository(ABC):
    @abstractmethod
    def create(self, export_receipt: ExportReceipt) -> ExportReceipt:
        pass

    @abstractmethod
    def get_by_id(self, export_receipt_id: int, household_id: int = None) -> Optional[ExportReceipt]:
        pass

    @abstractmethod
    def list(self, household_id: int) -> List[ExportReceipt]:
        pass

    @abstractmethod
    def update(self, export_receipt: ExportReceipt) -> ExportReceipt:
        pass
