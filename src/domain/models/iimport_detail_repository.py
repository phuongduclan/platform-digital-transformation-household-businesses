from abc import ABC, abstractmethod
from domain.models.import_detail import ImportDetail
from typing import List, Optional

class IImportDetailRepository(ABC):
    @abstractmethod
    def add(self, import_detail: ImportDetail) -> ImportDetail:
        pass

    @abstractmethod
    def get_by_id(self, import_detail_id: int, household_id: int = None) -> Optional[ImportDetail]:
        pass

    @abstractmethod
    def list_by_import_id(self, import_id: int, household_id: int = None) -> List[ImportDetail]:
        pass

    @abstractmethod
    def update(self, import_detail: ImportDetail, household_id: int = None) -> ImportDetail:
        pass
