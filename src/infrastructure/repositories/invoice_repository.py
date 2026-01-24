from domain.models.iinvoice_repository import IInvoiceRepository
from domain.models.invoice import Invoice
from typing import List, Optional
from infrastructure.models.invoice_model import Invoice as InvoiceModel
from infrastructure.databases.mssql import session

class InvoiceRepository(IInvoiceRepository):
    def __init__(self, session=session):
        self.session = session

    def create(self, invoice: Invoice) -> Invoice:
        try:
            invoice_model = InvoiceModel(
                household_id=invoice.household_id,
                seller_id=invoice.seller_id,
                customer_id=invoice.customer_id,
                invoice_type=invoice.invoice_type,
                discount_total=invoice.discount_total,
                vat_total=invoice.vat_total,
                total_amount=invoice.total_amount,
                description=invoice.description,
                status=invoice.status,
                created_by=invoice.created_by,
                updated_by=invoice.updated_by,
                created_at=invoice.created_at,
                updated_at=invoice.updated_at
            )
            self.session.add(invoice_model)
            self.session.flush()  # Flush để lấy ID, chưa commit
            self.session.refresh(invoice_model)
            return self._to_domain(invoice_model)
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error creating invoice: {str(e)}')

    def get_by_id(self, invoice_id: int, household_id: int = None) -> Optional[Invoice]:
        query = self.session.query(InvoiceModel).filter_by(id=invoice_id)
        if household_id is not None:
            query = query.filter_by(household_id=household_id)
        invoice_model = query.first()
        return self._to_domain(invoice_model) if invoice_model else None

    def list(self, household_id: int, status: Optional[str] = None) -> List[Invoice]:
        query = self.session.query(InvoiceModel).filter_by(household_id=household_id)
        if status:
            query = query.filter_by(status=status)
        invoice_models = query.all()
        return [self._to_domain(im) for im in invoice_models]

    def update(self, invoice: Invoice) -> Invoice:
        try:
            invoice_model = self.session.query(InvoiceModel).filter_by(
                id=invoice.id, household_id=invoice.household_id
            ).first()
            if not invoice_model:
                raise ValueError('Invoice not found')

            if invoice.seller_id is not None:
                invoice_model.seller_id = invoice.seller_id
            if invoice.customer_id is not None:
                invoice_model.customer_id = invoice.customer_id
            if invoice.invoice_type is not None:
                invoice_model.invoice_type = invoice.invoice_type
            if invoice.discount_total is not None:
                invoice_model.discount_total = invoice.discount_total
            if invoice.vat_total is not None:
                invoice_model.vat_total = invoice.vat_total
            if invoice.total_amount is not None:
                invoice_model.total_amount = invoice.total_amount
            if invoice.description is not None:
                invoice_model.description = invoice.description
            if invoice.status is not None:
                invoice_model.status = invoice.status
            if invoice.updated_by is not None:
                invoice_model.updated_by = invoice.updated_by
            if invoice.updated_at is not None:
                invoice_model.updated_at = invoice.updated_at

            self.session.flush()  # Flush, chưa commit
            self.session.refresh(invoice_model)
            return self._to_domain(invoice_model)
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error updating invoice: {str(e)}')

    def delete(self, invoice_id: int, household_id: int = None) -> None:
        try:
            query = self.session.query(InvoiceModel).filter_by(id=invoice_id)
            if household_id is not None:
                query = query.filter_by(household_id=household_id)
            invoice_model = query.first()
            if invoice_model:
                self.session.delete(invoice_model)
                self.session.commit()
            else:
                raise ValueError('Invoice not found')
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error deleting invoice: {str(e)}')

    def confirm(self, invoice_id: int, household_id: int = None, updated_by: str = None) -> Invoice:
        try:
            query = self.session.query(InvoiceModel).filter_by(id=invoice_id)
            if household_id is not None:
                query = query.filter_by(household_id=household_id)
            invoice_model = query.first()
            if not invoice_model:
                raise ValueError('Invoice not found')

            if invoice_model.status != 'Draft':
                raise ValueError('Only Draft invoices can be confirmed')

            invoice_model.status = 'Confirm'
            if updated_by is not None:
                invoice_model.updated_by = updated_by
            from datetime import datetime
            from infrastructure.utils.datetime_utils import vietnam_now
            invoice_model.updated_at = vietnam_now()
            self.session.flush()  # Flush, chưa commit
            self.session.refresh(invoice_model)
            return self._to_domain(invoice_model)
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error confirming invoice: {str(e)}')

    def _to_domain(self, invoice_model: InvoiceModel) -> Invoice:
        return Invoice(
            id=invoice_model.id,
            household_id=invoice_model.household_id,
            seller_id=invoice_model.seller_id,
            customer_id=invoice_model.customer_id,
            invoice_type=invoice_model.invoice_type,
            discount_total=invoice_model.discount_total,
            vat_total=invoice_model.vat_total,
            total_amount=invoice_model.total_amount,
            description=invoice_model.description,
            status=invoice_model.status,
            created_by=invoice_model.created_by,
            updated_by=invoice_model.updated_by,
            created_at=invoice_model.created_at,
            updated_at=invoice_model.updated_at
        )
