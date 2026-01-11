from domain.models.iinvoice_detail_repository import IInvoiceDetailRepository
from domain.models.invoice_detail import InvoiceDetail
from typing import List, Optional
from infrastructure.models.invoice_detail_model import InvoiceDetail as InvoiceDetailModel
from infrastructure.models.invoice_model import Invoice as InvoiceModel
from infrastructure.databases.mssql import session

class InvoiceDetailRepository(IInvoiceDetailRepository):
    def __init__(self, session=session):
        self.session = session

    def add(self, invoice_detail: InvoiceDetail) -> InvoiceDetail:
        try:
            invoice_detail_model = InvoiceDetailModel(
                invoice_id=invoice_detail.invoice_id,
                product_id=invoice_detail.product_id,
                unit_id=invoice_detail.unit_id,
                vat=invoice_detail.vat,
                discount=invoice_detail.discount,
                price=invoice_detail.price,
                description=invoice_detail.description,
                quantity=invoice_detail.quantity,
                status=invoice_detail.status,
                created_at=invoice_detail.created_at,
                updated_at=invoice_detail.updated_at
            )
            self.session.add(invoice_detail_model)
            self.session.flush()  # Flush để lấy ID, chưa commit
            self.session.refresh(invoice_detail_model)
            return self._to_domain(invoice_detail_model)
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error creating invoice detail: {str(e)}')

    def get_by_id(self, invoice_detail_id: int, household_id: int = None) -> Optional[InvoiceDetail]:
        query = self.session.query(InvoiceDetailModel).filter_by(id=invoice_detail_id)
        if household_id is not None:
            query = query.join(InvoiceModel).filter(InvoiceModel.household_id == household_id)
        invoice_detail_model = query.first()
        return self._to_domain(invoice_detail_model) if invoice_detail_model else None

    def list_by_invoice_id(self, invoice_id: int, household_id: int = None) -> List[InvoiceDetail]:
        query = self.session.query(InvoiceDetailModel).filter_by(invoice_id=invoice_id)
        if household_id is not None:
            query = query.join(InvoiceModel).filter(InvoiceModel.household_id == household_id)
        invoice_detail_models = query.all()
        return [self._to_domain(idm) for idm in invoice_detail_models]

    def update(self, invoice_detail: InvoiceDetail, household_id: int = None) -> InvoiceDetail:
        try:
            query = self.session.query(InvoiceDetailModel).filter_by(id=invoice_detail.id)
            if household_id is not None:
                query = query.join(InvoiceModel).filter(InvoiceModel.household_id == household_id)
            invoice_detail_model = query.first()
            if not invoice_detail_model:
                raise ValueError('Invoice detail not found')

            if invoice_detail.product_id is not None:
                invoice_detail_model.product_id = invoice_detail.product_id
            if invoice_detail.unit_id is not None:
                invoice_detail_model.unit_id = invoice_detail.unit_id
            if invoice_detail.vat is not None:
                invoice_detail_model.vat = invoice_detail.vat
            if invoice_detail.discount is not None:
                invoice_detail_model.discount = invoice_detail.discount
            if invoice_detail.price is not None:
                invoice_detail_model.price = invoice_detail.price
            if invoice_detail.description is not None:
                invoice_detail_model.description = invoice_detail.description
            if invoice_detail.quantity is not None:
                invoice_detail_model.quantity = invoice_detail.quantity
            if invoice_detail.status is not None:
                invoice_detail_model.status = invoice_detail.status
            if invoice_detail.updated_at is not None:
                invoice_detail_model.updated_at = invoice_detail.updated_at

            self.session.flush()  # Flush, chưa commit
            self.session.refresh(invoice_detail_model)
            return self._to_domain(invoice_detail_model)
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error updating invoice detail: {str(e)}')

    def delete(self, invoice_detail_id: int, household_id: int = None) -> None:
        try:
            query = self.session.query(InvoiceDetailModel).filter_by(id=invoice_detail_id)
            if household_id is not None:
                query = query.join(InvoiceModel).filter(InvoiceModel.household_id == household_id)
            invoice_detail_model = query.first()
            if invoice_detail_model:
                self.session.delete(invoice_detail_model)
                self.session.commit()
            else:
                raise ValueError('Invoice detail not found')
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error deleting invoice detail: {str(e)}')

    def _to_domain(self, invoice_detail_model: InvoiceDetailModel) -> InvoiceDetail:
        return InvoiceDetail(
            id=invoice_detail_model.id,
            invoice_id=invoice_detail_model.invoice_id,
            product_id=invoice_detail_model.product_id,
            unit_id=invoice_detail_model.unit_id,
            vat=invoice_detail_model.vat,
            discount=invoice_detail_model.discount,
            price=invoice_detail_model.price,
            description=invoice_detail_model.description,
            quantity=invoice_detail_model.quantity,
            status=invoice_detail_model.status,
            created_at=invoice_detail_model.created_at,
            updated_at=invoice_detail_model.updated_at
        )
