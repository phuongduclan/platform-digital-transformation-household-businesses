from abc import ABC, abstractmethod
from .invoice import Invoice
from typing import List, Optional

class IInvoiceRepository(ABC):
    """Abstract interface for Invoice repository"""
    
    @abstractmethod
    def create(self, invoice: Invoice) -> Invoice:
        """Create a new invoice"""
        pass
    
    @abstractmethod
    def get_by_id(self, invoice_id: int) -> Optional[Invoice]:
        """Get invoice by ID"""
        pass
    
    @abstractmethod
    def list_all(self) -> List[Invoice]:
        """List all invoices (Owner only)"""
        pass
    
    @abstractmethod
    def list_by_user(self, user_id: int) -> List[Invoice]:
        """List invoices created by specific user (Employee)"""
        pass
    
    @abstractmethod
    def list_draft_orders(self) -> List[Invoice]:
        """List draft orders from AI"""
        pass
    
    @abstractmethod
    def update(self, invoice: Invoice) -> Invoice:
        """Update an existing invoice"""
        pass
    
    @abstractmethod
    def delete(self, invoice_id: int) -> None:
        """Delete an invoice"""
        pass
    
    @abstractmethod
    def confirm(self, invoice_id: int) -> Invoice:
        """Confirm a draft invoice (change status to CONFIRMED)"""
        pass
