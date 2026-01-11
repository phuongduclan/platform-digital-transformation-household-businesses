from abc import ABC, abstractmethod
from .invoice_detail import InvoiceDetail
from typing import List, Optional

class IInvoiceDetailRepository(ABC):
    """Abstract interface for InvoiceDetail repository"""
    
    @abstractmethod
    def create(self, invoice_detail: InvoiceDetail) -> InvoiceDetail:
        """Create a new invoice detail"""
        pass
    
    @abstractmethod
    def get_by_id(self, detail_id: int) -> Optional[InvoiceDetail]:
        """Get invoice detail by ID"""
        pass
    
    @abstractmethod
    def list_by_invoice(self, invoice_id: int) -> List[InvoiceDetail]:
        """List all details for a specific invoice"""
        pass
    
    @abstractmethod
    def update(self, invoice_detail: InvoiceDetail) -> InvoiceDetail:
        """Update an existing invoice detail"""
        pass
    
    @abstractmethod
    def delete(self, detail_id: int) -> None:
        """Delete an invoice detail"""
        pass
