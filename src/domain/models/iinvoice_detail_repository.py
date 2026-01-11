from abc import ABC, abstractmethod
from .invoice_detail import InvoiceDetail
from typing import List, Optional

class IInvoiceDetailRepository(ABC):
    @abstractmethod
    def add(self, invoice_detail: InvoiceDetail) -> InvoiceDetail:
        pass

    @abstractmethod
    def get_by_id(self, invoice_detail_id: int, household_id: int = None) -> Optional[InvoiceDetail]:
        pass

    @abstractmethod
    def list_by_invoice_id(self, invoice_id: int, household_id: int = None) -> List[InvoiceDetail]:
        pass

    @abstractmethod
    def update(self, invoice_detail: InvoiceDetail) -> InvoiceDetail:
        pass

    @abstractmethod
    def delete(self, invoice_detail_id: int, household_id: int = None) -> None:
        pass
