from domain.models.iinvoice_repository import IInvoiceRepository
from domain.models.invoice import Invoice
from typing import List, Optional
from sqlalchemy.orm import Session
from infrastructure.models.invoice_model import InvoiceModel
from infrastructure.databases.factory_database import FactoryDatabase as db_factory
from datetime import datetime

class InvoiceRepository(IInvoiceRepository):
    """Implementation of IInvoiceRepository using SQLAlchemy"""
    
    def __init__(self, session: Session = None):
        self.session = session or db_factory.get_database('POSTGREE').session
    
    def create(self, invoice: Invoice) -> Invoice:
        """Create a new invoice"""
        try:
            invoice_model = InvoiceModel(
                invoice_number=invoice.invoice_number,
                customer_name=invoice.customer_name,
                total_amount=invoice.total_amount,
                status=invoice.status,
                source=invoice.source,
                created_by=invoice.created_by,
                created_at=invoice.created_at,
                updated_at=invoice.updated_at
            )
            self.session.add(invoice_model)
            self.session.commit()
            self.session.refresh(invoice_model)
            
            # Map back to domain entity
            invoice.id = invoice_model.id
            return invoice
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Failed to create invoice: {str(e)}')
        finally:
            self.session.close()
    
    def get_by_id(self, invoice_id: int) -> Optional[Invoice]:
        """Get invoice by ID"""
        try:
            invoice_model = self.session.query(InvoiceModel).filter_by(id=invoice_id).first()
            if not invoice_model:
                return None
            
            return self._to_domain(invoice_model)
        except Exception as e:
            raise ValueError(f'Failed to get invoice: {str(e)}')
    
    def list_all(self) -> List[Invoice]:
        """List all invoices (Owner only)"""
        try:
            invoice_models = self.session.query(InvoiceModel).all()
            return [self._to_domain(model) for model in invoice_models]
        except Exception as e:
            raise ValueError(f'Failed to list invoices: {str(e)}')
    
    def list_by_user(self, user_id: int) -> List[Invoice]:
        """List invoices created by specific user (Employee)"""
        try:
            invoice_models = self.session.query(InvoiceModel).filter_by(created_by=user_id).all()
            return [self._to_domain(model) for model in invoice_models]
        except Exception as e:
            raise ValueError(f'Failed to list user invoices: {str(e)}')
    
    def list_draft_orders(self) -> List[Invoice]:
        """List draft orders from AI"""
        try:
            invoice_models = self.session.query(InvoiceModel).filter_by(
                source='AI',
                status='DRAFT'
            ).all()
            return [self._to_domain(model) for model in invoice_models]
        except Exception as e:
            raise ValueError(f'Failed to list draft orders: {str(e)}')
    
    def update(self, invoice: Invoice) -> Invoice:
        """Update an existing invoice"""
        try:
            invoice_model = self.session.query(InvoiceModel).filter_by(id=invoice.id).first()
            if not invoice_model:
                raise ValueError('Invoice not found')
            
            invoice_model.invoice_number = invoice.invoice_number
            invoice_model.customer_name = invoice.customer_name
            invoice_model.total_amount = invoice.total_amount
            invoice_model.status = invoice.status
            invoice_model.source = invoice.source
            invoice_model.updated_at = datetime.utcnow()
            
            self.session.commit()
            self.session.refresh(invoice_model)
            
            return self._to_domain(invoice_model)
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Failed to update invoice: {str(e)}')
        finally:
            self.session.close()
    
    def delete(self, invoice_id: int) -> None:
        """Delete an invoice"""
        try:
            invoice_model = self.session.query(InvoiceModel).filter_by(id=invoice_id).first()
            if not invoice_model:
                raise ValueError('Invoice not found')
            
            self.session.delete(invoice_model)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Failed to delete invoice: {str(e)}')
        finally:
            self.session.close()
    
    def confirm(self, invoice_id: int) -> Invoice:
        """Confirm a draft invoice (change status to CONFIRMED)"""
        try:
            invoice_model = self.session.query(InvoiceModel).filter_by(id=invoice_id).first()
            if not invoice_model:
                raise ValueError('Invoice not found')
            
            if invoice_model.status != 'DRAFT':
                raise ValueError('Only draft invoices can be confirmed')
            
            invoice_model.status = 'CONFIRMED'
            invoice_model.updated_at = datetime.utcnow()
            
            self.session.commit()
            self.session.refresh(invoice_model)
            
            return self._to_domain(invoice_model)
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Failed to confirm invoice: {str(e)}')
        finally:
            self.session.close()
    
    def _to_domain(self, model: InvoiceModel) -> Invoice:
        """Convert SQLAlchemy model to domain entity"""
        return Invoice(
            id=model.id,
            invoice_number=model.invoice_number,
            customer_name=model.customer_name,
            total_amount=model.total_amount,
            status=model.status,
            source=model.source,
            created_by=model.created_by,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
