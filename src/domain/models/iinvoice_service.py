from abc import ABC, abstractmethod
from domain.models.invoice import Invoice
from typing import List, Optional, Dict

class IInvoiceService(ABC):
    @abstractmethod
    def create_invoice_with_details(self, household_id: int, seller_id: int = None, customer_id: int = None,
                                    invoice_type: str = 'PAID', description: str = None, status: str = 'Draft',
                                    created_by: str = None, details: List[dict] = None) -> Invoice:
        pass

    @abstractmethod
    def get_invoice(self, invoice_id: int, household_id: int) -> Optional[Invoice]:
        pass

    @abstractmethod
    def list_invoices(self, household_id: int, status: Optional[str] = None) -> List[Invoice]:
        pass

    @abstractmethod
    def update_invoice(self, invoice_id: int, household_id: int, seller_id: int = None,
                       customer_id: int = None, invoice_type: str = None, description: str = None,
                       updated_by: str = None) -> Invoice:
        pass

    @abstractmethod
    def delete_invoice(self, invoice_id: int, household_id: int) -> None:
        pass

    @abstractmethod
    def confirm_invoice(self, invoice_id: int, household_id: int, updated_by: str = None,
                       import_receipt_service=None, export_receipt_service=None,
                       inventory_service=None, warehouse_repository=None,
                       debt_record_service=None, accounting_ledger_service=None,
                       seller_repository=None, customer_repository=None) -> Invoice:
        pass
