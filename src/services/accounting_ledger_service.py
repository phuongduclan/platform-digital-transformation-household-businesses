from domain.models.accounting_ledger import AccountingLedger
from domain.models.iaccounting_ledger_repository import IAccountingLedgerRepository
from domain.models.iaccounting_ledger_service import IAccountingLedgerService
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

class AccountingLedgerService(IAccountingLedgerService):
    def __init__(self, repository: IAccountingLedgerRepository):
        self.repository = repository

    def get_accounting_ledger(self, accounting_ledger_id: int, household_id: int) -> Optional[AccountingLedger]:
        return self.repository.get_by_id(accounting_ledger_id, household_id)

    def list_accounting_ledgers(self, household_id: int, from_date: datetime = None,
                               to_date: datetime = None, movement_type: str = None) -> List[AccountingLedger]:
        """List accounting ledgers (Owner chỉ xem, không được tạo thủ công)"""
        return self.repository.list(household_id, from_date, to_date, movement_type)

    def get_by_invoice_id(self, invoice_id: int, household_id: int) -> Optional[AccountingLedger]:
        """Lấy accounting ledger theo invoice_id"""
        return self.repository.get_by_invoice_id(invoice_id, household_id)

    def create_accounting_ledger(self, invoice_id: int, transaction_date: datetime,
                                 debit_amount: Decimal = None, credit_amount: Decimal = None,
                                 description: str = None, movement_type: str = None,
                                 household_id: int = None) -> AccountingLedger:
        """
        Tự động tạo AccountingLedger (không được gọi thủ công từ API).
        Được gọi tự động khi Invoice confirm hoặc Payment được tạo.
        """
        # Lấy balance hiện tại
        previous_balance = self._get_last_balance(household_id)
        
        # Tính balance mới
        if debit_amount is not None:
            new_balance = previous_balance - debit_amount  # Chi giảm balance
        elif credit_amount is not None:
            new_balance = previous_balance + credit_amount  # Thu tăng balance
        else:
            raise ValueError('AccountingLedger must have either debit_amount or credit_amount')
        
        accounting_ledger = AccountingLedger(
            id=None,
            invoice_id=invoice_id,
            transaction_date=transaction_date,
            description=description,
            debit_amount=debit_amount,
            credit_amount=credit_amount,
            balance=new_balance,
            document_number="",  # TODO: Generate theo thông tư 88/2021/TT-BTC
            movement_type=movement_type,
            status='Confirm',
            created_at=transaction_date,
            updated_at=transaction_date
        )
        
        return self.repository.create(accounting_ledger)

    def get_daily_revenue(self, household_id: int, date: datetime) -> Decimal:
        """Tính tổng doanh thu trong ngày (chỉ hóa đơn bán đã thanh toán)"""
        from datetime import timedelta
        start_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=1)
        
        ledgers = self.repository.list(household_id, start_date, end_date, 'Thu')
        total = sum(ledger.credit_amount for ledger in ledgers if ledger.credit_amount)
        return total or Decimal('0')

    def get_monthly_revenue(self, household_id: int, month: int, year: int) -> Decimal:
        """Tính tổng doanh thu trong tháng"""
        from datetime import timedelta
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)
        
        ledgers = self.repository.list(household_id, start_date, end_date, 'Thu')
        total = sum(ledger.credit_amount for ledger in ledgers if ledger.credit_amount)
        return total or Decimal('0')

    def _get_last_balance(self, household_id: int) -> Decimal:
        """Lấy balance mới nhất của accounting ledger"""
        ledgers = self.repository.list(household_id)
        return ledgers[0].balance if ledgers and ledgers[0].balance else Decimal('0')
