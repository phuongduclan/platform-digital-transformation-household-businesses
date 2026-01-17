from abc import ABC, abstractmethod
from domain.models.export_receipt import ExportReceipt
from typing import List, Optional
from datetime import date

class IExportReceiptService(ABC):
    @abstractmethod
    def create_export_receipt_with_details(self, warehouse_id: int, invoice_id: int = None,
                                           export_date: date = None, reason: str = None,
                                           details: List[dict] = None) -> ExportReceipt:
        pass

    @abstractmethod
    def get_export_receipt(self, export_receipt_id: int, household_id: int) -> Optional[ExportReceipt]:
        pass

    @abstractmethod
    def list_export_receipts(self, household_id: int) -> List[ExportReceipt]:
        pass

    @abstractmethod
    def update_export_receipt(self, export_receipt_id: int, household_id: int,
                              warehouse_id: int = None, export_date: date = None,
                              reason: str = None) -> ExportReceipt:
        pass
