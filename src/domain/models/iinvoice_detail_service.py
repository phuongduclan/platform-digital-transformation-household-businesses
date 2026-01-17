from abc import ABC, abstractmethod
from domain.models.invoice_detail import InvoiceDetail
from typing import List, Optional
from decimal import Decimal

class IInvoiceDetailService(ABC):
    @abstractmethod
    def create_invoice_detail(self, invoice_id: int, product_id: int, unit_id: int,
                              quantity: int, price: Decimal, vat: int = 0, discount: int = 0,
                              description: str = None, status: str = 'Draft',
                              household_id: int = None) -> InvoiceDetail:
        pass

    @abstractmethod
    def get_invoice_detail(self, invoice_detail_id: int, household_id: int = None) -> Optional[InvoiceDetail]:
        pass

    @abstractmethod
    def list_invoice_details(self, invoice_id: int, household_id: int = None) -> List[InvoiceDetail]:
        pass

    @abstractmethod
    def update_invoice_detail(self, invoice_detail_id: int, household_id: int = None,
                              product_id: int = None, unit_id: int = None, quantity: int = None,
                              price: Decimal = None, vat: int = None, discount: int = None,
                              description: str = None) -> InvoiceDetail:
        pass

    @abstractmethod
    def delete_invoice_detail(self, invoice_detail_id: int, household_id: int = None) -> None:
        pass
