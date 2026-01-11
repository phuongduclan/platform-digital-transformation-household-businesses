from abc import ABC, abstractmethod
from domain.models.export_detail import ExportDetail
from typing import List, Optional

class IExportDetailRepository(ABC):
    @abstractmethod
    def add(self, export_detail: ExportDetail) -> ExportDetail:
        pass

    @abstractmethod
    def get_by_id(self, export_detail_id: int, household_id: int = None) -> Optional[ExportDetail]:
        pass

    @abstractmethod
    def list_by_export_id(self, export_id: int, household_id: int = None) -> List[ExportDetail]:
        pass

    @abstractmethod
    def update(self, export_detail: ExportDetail, household_id: int = None) -> ExportDetail:
        pass
