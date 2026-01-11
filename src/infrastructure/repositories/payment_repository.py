from domain.models.ipayment_repository import IPaymentRepository
from domain.models.payment import Payment
from typing import List, Optional
from infrastructure.models.payment_model import Payment as PaymentModel
from infrastructure.models.invoice_model import Invoice as InvoiceModel
from infrastructure.databases.mssql import session

class PaymentRepository(IPaymentRepository):
    def __init__(self, session=session):
        self.session = session

    def create(self, payment: Payment) -> Payment:
        try:
            payment_model = PaymentModel(
                invoice_id=payment.invoice_id,
                method_id=payment.method_id,
                amount=payment.amount,
                description=payment.description,
                status=payment.status,
                created_by=payment.created_by,
                updated_by=payment.updated_by,
                created_at=payment.created_at,
                updated_at=payment.updated_at
            )
            self.session.add(payment_model)
            self.session.flush()
            self.session.refresh(payment_model)
            return self._to_domain(payment_model)
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error creating payment: {str(e)}')

    def get_by_id(self, payment_id: int, household_id: int = None) -> Optional[Payment]:
        query = self.session.query(PaymentModel).filter_by(id=payment_id)
        if household_id is not None:
            query = query.join(InvoiceModel).filter(InvoiceModel.household_id == household_id)
        payment_model = query.first()
        return self._to_domain(payment_model) if payment_model else None

    def list(self, household_id: int, invoice_id: int = None, customer_id: int = None) -> List[Payment]:
        query = self.session.query(PaymentModel).join(InvoiceModel).filter(
            InvoiceModel.household_id == household_id
        )
        if invoice_id is not None:
            query = query.filter(PaymentModel.invoice_id == invoice_id)
        if customer_id is not None:
            query = query.filter(InvoiceModel.customer_id == customer_id)
        payment_models = query.all()
        return [self._to_domain(pm) for pm in payment_models]

    def update(self, payment: Payment, household_id: int = None) -> Payment:
        try:
            query = self.session.query(PaymentModel).filter_by(id=payment.id)
            if household_id is not None:
                query = query.join(InvoiceModel).filter(InvoiceModel.household_id == household_id)
            payment_model = query.first()
            if not payment_model:
                raise ValueError('Payment not found')

            if payment.method_id is not None:
                payment_model.method_id = payment.method_id
            if payment.amount is not None:
                payment_model.amount = payment.amount
            if payment.description is not None:
                payment_model.description = payment.description
            if payment.status is not None:
                payment_model.status = payment.status
            if payment.updated_by is not None:
                payment_model.updated_by = payment.updated_by
            if payment.updated_at is not None:
                payment_model.updated_at = payment.updated_at

            self.session.flush()
            self.session.refresh(payment_model)
            return self._to_domain(payment_model)
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error updating payment: {str(e)}')

    def delete(self, payment_id: int, household_id: int = None) -> None:
        try:
            query = self.session.query(PaymentModel).filter_by(id=payment_id)
            if household_id is not None:
                query = query.join(InvoiceModel).filter(InvoiceModel.household_id == household_id)
            payment_model = query.first()
            if payment_model:
                self.session.delete(payment_model)
                self.session.commit()
            else:
                raise ValueError('Payment not found')
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error deleting payment: {str(e)}')

    def _to_domain(self, payment_model: PaymentModel) -> Payment:
        return Payment(
            id=payment_model.id,
            invoice_id=payment_model.invoice_id,
            method_id=payment_model.method_id,
            amount=payment_model.amount,
            description=payment_model.description,
            status=payment_model.status,
            created_by=payment_model.created_by,
            updated_by=payment_model.updated_by,
            created_at=payment_model.created_at,
            updated_at=payment_model.updated_at
        )
