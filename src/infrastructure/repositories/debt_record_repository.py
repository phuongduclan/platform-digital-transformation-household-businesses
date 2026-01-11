from domain.models.idebt_record_repository import IDebtRecordRepository
from domain.models.debt_record import DebtRecord
from typing import List, Optional
from infrastructure.models.debt_record_model import DebtRecord as DebtRecordModel
from infrastructure.models.customer_model import Customer
from infrastructure.databases.mssql import session
from sqlalchemy import desc

class DebtRecordRepository(IDebtRecordRepository):
    def __init__(self, session=session):
        self.session = session

    def create(self, debt_record: DebtRecord) -> DebtRecord:
        try:
            debt_record_model = DebtRecordModel(
                customer_id=debt_record.customer_id,
                invoice_id=debt_record.invoice_id,
                payment_id=debt_record.payment_id,
                debit_amount=debt_record.debit_amount,
                credit_amount=debt_record.credit_amount,
                balance=debt_record.balance,
                description=debt_record.description,
                record_at=debt_record.record_at
            )
            self.session.add(debt_record_model)
            self.session.flush()
            self.session.refresh(debt_record_model)
            return self._to_domain(debt_record_model)
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error creating debt record: {str(e)}')

    def get_by_id(self, debt_record_id: int, household_id: int = None) -> Optional[DebtRecord]:
        query = self.session.query(DebtRecordModel).filter_by(id=debt_record_id)
        if household_id is not None:
            query = query.join(Customer).filter(Customer.household_id == household_id)
        debt_record_model = query.first()
        return self._to_domain(debt_record_model) if debt_record_model else None

    def list(self, household_id: int, customer_id: int = None) -> List[DebtRecord]:
        query = self.session.query(DebtRecordModel).join(Customer).filter(
            Customer.household_id == household_id
        )
        if customer_id is not None:
            query = query.filter(DebtRecordModel.customer_id == customer_id)
        query = query.order_by(desc(DebtRecordModel.record_at))
        debt_record_models = query.all()
        return [self._to_domain(drm) for drm in debt_record_models]

    def get_by_customer_id(self, customer_id: int, household_id: int = None) -> List[DebtRecord]:
        query = self.session.query(DebtRecordModel).filter_by(customer_id=customer_id)
        if household_id is not None:
            query = query.join(Customer).filter(Customer.household_id == household_id)
        query = query.order_by(desc(DebtRecordModel.record_at))
        debt_record_models = query.all()
        return [self._to_domain(drm) for drm in debt_record_models]

    def get_customer_balance(self, customer_id: int, household_id: int = None) -> Optional[DebtRecord]:
        """Lấy balance hiện tại của customer (bản ghi mới nhất)"""
        query = self.session.query(DebtRecordModel).filter_by(customer_id=customer_id)
        if household_id is not None:
            query = query.join(Customer).filter(Customer.household_id == household_id)
        query = query.order_by(desc(DebtRecordModel.record_at))
        debt_record_model = query.first()
        return self._to_domain(debt_record_model) if debt_record_model else None

    def _to_domain(self, debt_record_model: DebtRecordModel) -> DebtRecord:
        return DebtRecord(
            id=debt_record_model.id,
            customer_id=debt_record_model.customer_id,
            invoice_id=debt_record_model.invoice_id,
            payment_id=debt_record_model.payment_id,
            debit_amount=debt_record_model.debit_amount,
            credit_amount=debt_record_model.credit_amount,
            balance=debt_record_model.balance,
            description=debt_record_model.description,
            record_at=debt_record_model.record_at
        )
