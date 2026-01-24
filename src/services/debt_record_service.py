from domain.models.debt_record import DebtRecord
from domain.models.idebt_record_repository import IDebtRecordRepository
from domain.models.idebt_record_service import IDebtRecordService
from typing import List, Optional
from decimal import Decimal

class DebtRecordService(IDebtRecordService):
    def __init__(self, repository: IDebtRecordRepository):
        self.repository = repository

    def get_debt_record(self, debt_record_id: int, household_id: int) -> Optional[DebtRecord]:
        return self.repository.get_by_id(debt_record_id, household_id)

    def list_debt_records(self, household_id: int, customer_id: int = None) -> List[DebtRecord]:
        """List debt records (Owner/Employee chỉ xem, không được tạo thủ công)"""
        return self.repository.list(household_id, customer_id)

    def get_customer_debt_records(self, customer_id: int, household_id: int) -> List[DebtRecord]:
        """Lấy tất cả debt records của 1 customer"""
        return self.repository.get_by_customer_id(customer_id, household_id)

    def get_customer_balance(self, customer_id: int, household_id: int) -> Decimal:
        """Lấy balance hiện tại của customer"""
        last_record = self.repository.get_customer_balance(customer_id, household_id)
        return last_record.balance if last_record else Decimal('0')

    def create_debt_record(self, customer_id: int, invoice_id: int = None, payment_id: int = None,
                          debit_amount: Decimal = None, credit_amount: Decimal = None,
                          description: str = None, household_id: int = None) -> DebtRecord:
        """
        Tự động tạo DebtRecord (không được gọi thủ công từ API).
        Được gọi tự động khi Invoice confirm (UNPAID) hoặc Payment được tạo.
        """
        from datetime import datetime
from infrastructure.utils.datetime_utils import vietnam_now
        
        # Ràng buộc: một bản ghi chỉ nợ hoặc chỉ trả
        if invoice_id is not None and payment_id is not None:
            raise ValueError('DebtRecord cannot have both invoice_id and payment_id')
        if invoice_id is None and payment_id is None:
            raise ValueError('DebtRecord must have either invoice_id or payment_id')
        
        # Lấy balance hiện tại của customer
        previous_balance = self.get_customer_balance(customer_id, household_id)
        
        # Tính balance mới
        if debit_amount is not None:
            new_balance = previous_balance + debit_amount  # Nợ tăng balance
        elif credit_amount is not None:
            new_balance = previous_balance - credit_amount  # Trả giảm balance
        else:
            raise ValueError('DebtRecord must have either debit_amount or credit_amount')
        
        debt_record = DebtRecord(
            id=None,
            customer_id=customer_id,
            invoice_id=invoice_id,
            payment_id=payment_id,
            debit_amount=debit_amount,
            credit_amount=credit_amount,
            balance=new_balance,
            description=description,
            record_at=vietnam_now()
        )
        
        return self.repository.create(debt_record)
