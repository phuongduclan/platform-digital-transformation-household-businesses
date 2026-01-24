from domain.models.payment_method import PaymentMethod
from domain.models.ipayment_method_repository import IPaymentMethodRepository
from domain.models.ipayment_method_service import IPaymentMethodService
from typing import List, Optional

class PaymentMethodService(IPaymentMethodService):
    def __init__(self, repository: IPaymentMethodRepository):
        self.repository = repository

    def list_payment_methods(self, status: str = 'Active') -> List[PaymentMethod]:
        """List payment methods (Owner chỉ xem, Admin quản lý)"""
        return self.repository.list(status)

    def get_payment_method(self, payment_method_id: int) -> Optional[PaymentMethod]:
        return self.repository.get_by_id(payment_method_id)

    # Admin only methods
    def create_payment_method(self, name: str, status: str = 'Active') -> PaymentMethod:
        """Admin only: Create payment method"""
        from datetime import datetime
        from infrastructure.utils.datetime_utils import vietnam_now
        now = vietnam_now()
        payment_method = PaymentMethod(
            id=None,
            name=name,
            status=status,
            created_at=now,
            updated_at=now
        )
        return self.repository.create(payment_method)

    def update_payment_method(self, payment_method_id: int, name: str = None, status: str = None) -> PaymentMethod:
        """Admin only: Update payment method"""
        from datetime import datetime
        existing = self.repository.get_by_id(payment_method_id)
        if not existing:
            raise ValueError('Payment method not found')
        
        if name is not None:
            existing.name = name
        if status is not None:
            existing.status = status
        existing.updated_at = vietnam_now()
        
        return self.repository.update(existing)

    def delete_payment_method(self, payment_method_id: int) -> None:
        """Admin only: Delete payment method"""
        self.repository.delete(payment_method_id)
