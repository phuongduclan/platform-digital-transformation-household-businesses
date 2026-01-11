from abc import ABC, abstractmethod
from .invoice import Invoice
from typing import List, Optional

class IInvoiceRepository(ABC):
    @abstractmethod
    def create(self, invoice: Invoice) -> Invoice:
        pass

    @abstractmethod
    def get_by_id(self, invoice_id: int, household_id: int = None) -> Optional[Invoice]:
        pass

    @abstractmethod
    def list(self, household_id: int, status: Optional[str] = None) -> List[Invoice]:
        pass

    @abstractmethod
    def update(self, invoice: Invoice) -> Invoice:
        pass

    @abstractmethod
    def delete(self, invoice_id: int, household_id: int = None) -> None:
        pass

    @abstractmethod
    def confirm(self, invoice_id: int, household_id: int = None) -> Invoice:
        pass
