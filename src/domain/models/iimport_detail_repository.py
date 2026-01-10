from abc import ABC, abstractmethod
from typing import List
from .import_detail import ImportDetail


class IImportDetailRepository(ABC):

    @abstractmethod
    def get_by_receipt_id(self, receipt_id: int) -> List[ImportDetail]:
        pass

    @abstractmethod
    def add(self, detail: ImportDetail) -> None:
        pass
