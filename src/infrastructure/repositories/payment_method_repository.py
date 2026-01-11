from domain.models.ipayment_method_repository import IPaymentMethodRepository
from domain.models.payment_method import PaymentMethod
from typing import List, Optional
from infrastructure.models.paymentmethod_model import PaymentMethod as PaymentMethodModel
from infrastructure.databases.mssql import session

class PaymentMethodRepository(IPaymentMethodRepository):
    def __init__(self, session=session):
        self.session = session

    def create(self, payment_method: PaymentMethod) -> PaymentMethod:
        try:
            payment_method_model = PaymentMethodModel(
                name=payment_method.name,
                status=payment_method.status,
                created_at=payment_method.created_at,
                updated_at=payment_method.updated_at
            )
            self.session.add(payment_method_model)
            self.session.commit()
            self.session.refresh(payment_method_model)
            return self._to_domain(payment_method_model)
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error creating payment method: {str(e)}')

    def get_by_id(self, payment_method_id: int) -> Optional[PaymentMethod]:
        payment_method_model = self.session.query(PaymentMethodModel).filter_by(id=payment_method_id).first()
        return self._to_domain(payment_method_model) if payment_method_model else None

    def list(self, status: str = 'Active') -> List[PaymentMethod]:
        query = self.session.query(PaymentMethodModel)
        if status:
            query = query.filter_by(status=status)
        payment_method_models = query.all()
        return [self._to_domain(pmm) for pmm in payment_method_models]

    def update(self, payment_method: PaymentMethod) -> PaymentMethod:
        try:
            payment_method_model = self.session.query(PaymentMethodModel).filter_by(id=payment_method.id).first()
            if not payment_method_model:
                raise ValueError('Payment method not found')

            if payment_method.name is not None:
                payment_method_model.name = payment_method.name
            if payment_method.status is not None:
                payment_method_model.status = payment_method.status
            if payment_method.updated_at is not None:
                payment_method_model.updated_at = payment_method.updated_at

            self.session.commit()
            self.session.refresh(payment_method_model)
            return self._to_domain(payment_method_model)
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error updating payment method: {str(e)}')

    def delete(self, payment_method_id: int) -> None:
        try:
            payment_method_model = self.session.query(PaymentMethodModel).filter_by(id=payment_method_id).first()
            if payment_method_model:
                self.session.delete(payment_method_model)
                self.session.commit()
            else:
                raise ValueError('Payment method not found')
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error deleting payment method: {str(e)}')

    def _to_domain(self, payment_method_model: PaymentMethodModel) -> PaymentMethod:
        return PaymentMethod(
            id=payment_method_model.id,
            name=payment_method_model.name,
            status=payment_method_model.status,
            created_at=payment_method_model.created_at,
            updated_at=payment_method_model.updated_at
        )
