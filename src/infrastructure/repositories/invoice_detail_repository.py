from domain.models.iinvoice_detail_repository import IInvoiceDetailRepository
from domain.models.invoice_detail import InvoiceDetail
from typing import List, Optional
from infrastructure.models import InvoiceDetail as InvoiceDetailModel, Invoice as InvoiceModel
from infrastructure.databases.mssql import session

class InvoiceDetailRepository(IInvoiceDetailRepository):
    """Implementation of IInvoiceDetailRepository using SQLAlchemy"""
    
    def __init__(self, db_session=session):
        self.session = db_session
    
    def create(self, invoice_detail: InvoiceDetail) -> InvoiceDetail:
        """Create a new invoice detail"""
        try:
            # Verify invoice exists
            invoice = self.session.query(InvoiceModel).filter_by(id=invoice_detail.invoice_id).first()
            if not invoice:
                raise ValueError('Invoice not found')
            
            detail_model = InvoiceDetailModel(
                invoice_id=invoice_detail.invoice_id,
                product_name=invoice_detail.product_name,
                quantity=invoice_detail.quantity,
                unit_price=invoice_detail.unit_price,
                vat=invoice_detail.vat,
                discount=invoice_detail.discount,
                description=invoice_detail.description,
                subtotal=invoice_detail.subtotal
            )
            self.session.add(detail_model)
            
            # Update invoice total
            invoice.total_amount += invoice_detail.subtotal
            
            self.session.commit()
            self.session.refresh(detail_model)
            
            # Map back to domain entity
            invoice_detail.id = detail_model.id
            return invoice_detail
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Failed to create invoice detail: {str(e)}')
    
    def get_by_id(self, detail_id: int) -> Optional[InvoiceDetail]:
        """Get invoice detail by ID"""
        try:
            detail_model = self.session.query(InvoiceDetailModel).filter_by(id=detail_id).first()
            if not detail_model:
                return None
            
            return self._to_domain(detail_model)
        except Exception as e:
            raise ValueError(f'Failed to get invoice detail: {str(e)}')
    
    def list_by_invoice(self, invoice_id: int) -> List[InvoiceDetail]:
        """List all details for a specific invoice"""
        try:
            detail_models = self.session.query(InvoiceDetailModel).filter_by(invoice_id=invoice_id).all()
            return [self._to_domain(model) for model in detail_models]
        except Exception as e:
            raise ValueError(f'Failed to list invoice details: {str(e)}')
    
    def update(self, invoice_detail: InvoiceDetail) -> InvoiceDetail:
        """Update an existing invoice detail"""
        try:
            detail_model = self.session.query(InvoiceDetailModel).filter_by(id=invoice_detail.id).first()
            if not detail_model:
                raise ValueError('Invoice detail not found')
            
            # Calculate difference for invoice total update
            old_subtotal = detail_model.subtotal
            new_subtotal = invoice_detail.subtotal
            difference = new_subtotal - old_subtotal
            
            # Update detail
            detail_model.product_name = invoice_detail.product_name
            detail_model.quantity = invoice_detail.quantity
            detail_model.unit_price = invoice_detail.unit_price
            detail_model.vat = invoice_detail.vat
            detail_model.discount = invoice_detail.discount
            detail_model.description = invoice_detail.description
            detail_model.subtotal = invoice_detail.subtotal
            
            # Update invoice total
            invoice = self.session.query(InvoiceModel).filter_by(id=detail_model.invoice_id).first()
            if invoice:
                invoice.total_amount += difference
            
            self.session.commit()
            self.session.refresh(detail_model)
            
            return self._to_domain(detail_model)
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Failed to update invoice detail: {str(e)}')
    
    def delete(self, detail_id: int) -> None:
        """Delete an invoice detail"""
        try:
            detail_model = self.session.query(InvoiceDetailModel).filter_by(id=detail_id).first()
            if not detail_model:
                raise ValueError('Invoice detail not found')
            
            # Update invoice total
            invoice = self.session.query(InvoiceModel).filter_by(id=detail_model.invoice_id).first()
            if invoice:
                invoice.total_amount -= detail_model.subtotal
            
            self.session.delete(detail_model)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Failed to delete invoice detail: {str(e)}')
    
    def _to_domain(self, model: InvoiceDetailModel) -> InvoiceDetail:
        """Convert SQLAlchemy model to domain entity"""
        return InvoiceDetail(
            id=model.id,
            invoice_id=model.invoice_id,
            product_name=model.product_name,
            quantity=model.quantity,
            unit_price=float(model.unit_price),
            vat=float(model.vat) if model.vat else 0.0,
            discount=float(model.discount) if model.discount else 0.0,
            description=model.description,
            subtotal=float(model.subtotal)
        )
