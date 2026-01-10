from abc import ABC, abstractmethod
from typing import List
from .export_detail import ExportDetail


class IExportDetailRepository(ABC):

    @abstractmethod
    def get_by_receipt_id(self, receipt_id: int) -> List[ExportDetail]:
        pass

    @abstractmethod
    def add(self, detail: ExportDetail) -> None:
        pass
