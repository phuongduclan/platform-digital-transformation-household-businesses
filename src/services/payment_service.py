from domain.models.payment import Payment
from domain.models.ipayment_repository import IPaymentRepository
from domain.models.iinvoice_repository import IInvoiceRepository
from domain.models.idebt_record_repository import IDebtRecordRepository
from domain.models.iaccounting_ledger_repository import IAccountingLedgerRepository
from domain.models.ipayment_service import IPaymentService
# from domain.models.icustomer_repository import ICustomerRepository  # TODO: Import khi có CustomerRepository
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

class PaymentService(IPaymentService):
    def __init__(self, repository: IPaymentRepository, invoice_repository: IInvoiceRepository,
                 debt_record_repository: IDebtRecordRepository = None,
                 accounting_ledger_repository: IAccountingLedgerRepository = None,
                 customer_repository = None):
        self.repository = repository
        self.invoice_repository = invoice_repository
        self.debt_record_repository = debt_record_repository
        self.accounting_ledger_repository = accounting_ledger_repository
        self.customer_repository = customer_repository

    def create_payment(self, invoice_id: int, method_id: int, amount: Decimal,
                      description: str = None, created_by: str = None,
                      household_id: int = None) -> Payment:
        """
        Tạo Payment cho hóa đơn bán chịu (UNPAID).
        Chỉ cho phép tạo Payment cho hóa đơn có customer_id và invoice_type = 'UNPAID'.
        Tự động tạo DebtRecord và AccountingLedger trong 1 transaction.
        """
        # Kiểm tra invoice tồn tại và là hóa đơn bán
        invoice = self.invoice_repository.get_by_id(invoice_id, household_id)
        if not invoice:
            raise ValueError('Invoice not found')
        
        if invoice.customer_id is None:
            raise ValueError('Payment chỉ được tạo cho hóa đơn có khách hàng trong bảng customer (không áp dụng cho khách vãng lai)')
        
        if invoice.status != 'Confirm':
            raise ValueError('Payment chỉ được tạo cho hóa đơn đã confirm')
        
        if invoice.invoice_type != 'UNPAID':
            raise ValueError('Payment chỉ được tạo cho hóa đơn bán chịu (invoice_type = UNPAID). Hóa đơn đã thanh toán đủ (PAID) không cần Payment')
        
        # Lấy session từ repository để quản lý transaction
        db_session = getattr(self.repository, 'session', None)
        if not db_session:
            raise ValueError("Repository must have a session attribute")
        
        # Đảm bảo các repositories dùng cùng session
        if self.debt_record_repository and hasattr(self.debt_record_repository, 'session'):
            self.debt_record_repository.session = db_session
        if self.accounting_ledger_repository and hasattr(self.accounting_ledger_repository, 'session'):
            self.accounting_ledger_repository.session = db_session
        
        try:
            now = datetime.utcnow()
            
            # Tạo Payment
            payment = Payment(
                id=None,
                invoice_id=invoice_id,
                method_id=method_id,
                amount=amount,
                description=description,
                status='Confirm',
                created_by=created_by,
                updated_by=created_by,
                created_at=now,
                updated_at=now
            )
            payment = self.repository.create(payment)
            
            # Tự động tạo DebtRecord (nếu có customer_id)
            if self.debt_record_repository and invoice.customer_id:
                # Lấy balance hiện tại của customer
                last_debt_record = self.debt_record_repository.get_customer_balance(
                    invoice.customer_id, household_id
                )
                previous_balance = last_debt_record.balance if last_debt_record else Decimal('0')

                # Chặn thanh toán nếu không còn dư nợ hoặc thanh toán vượt quá dư nợ
                if previous_balance <= 0:
                    raise ValueError('Khách hàng hiện không còn dư nợ để thanh toán thêm')
                if amount > previous_balance:
                    raise ValueError(
                        f'Số tiền thanh toán vượt quá số nợ còn lại. '
                        f'Nợ còn lại: {previous_balance}, thanh toán yêu cầu: {amount}'
                    )

                new_balance = previous_balance - amount  # Trả nợ nên giảm balance
                
                debt_record = self.debt_record_repository.create(
                    self._create_debt_record(
                        customer_id=invoice.customer_id,
                        payment_id=payment.id,
                        credit_amount=amount,
                        balance=new_balance,
                        description=description or f"Thanh toán hóa đơn #{invoice_id}"
                    )
                )
            
            # Tự động tạo AccountingLedger
            if self.accounting_ledger_repository:
                # Lấy customer name
                customer_name = "Khách hàng"
                if self.customer_repository and invoice.customer_id:
                    customer = self.customer_repository.get_by_id(invoice.customer_id, household_id)
                    if customer:
                        customer_name = customer.name or "Khách hàng"
                
                # Lấy balance hiện tại của accounting ledger
                last_ledger = self._get_last_ledger_balance(household_id)
                previous_balance = last_ledger.balance if last_ledger else Decimal('0')
                new_balance = previous_balance + amount  # Thu nên tăng balance
                
                accounting_ledger = self.accounting_ledger_repository.create(
                    self._create_accounting_ledger(
                        invoice_id=invoice_id,
                        transaction_date=now,
                        credit_amount=amount,
                        balance=new_balance,
                        description=f"Thu từ {customer_name} - HĐ #{invoice_id} - Payment #{payment.id}",
                        movement_type='Thu'
                    )
                )

            # Nếu sau khi thanh toán, tổng dư nợ của customer về 0 → cập nhật invoice_type = PAID
            if self.debt_record_repository and invoice.customer_id:
                last_debt_record_after = self.debt_record_repository.get_customer_balance(
                    invoice.customer_id, household_id
                )
                remaining_balance = last_debt_record_after.balance if last_debt_record_after else Decimal('0')
                if remaining_balance == 0:
                    invoice.invoice_type = 'PAID'
                    invoice.updated_by = created_by
                    invoice.updated_at = now
                    if hasattr(self.invoice_repository, 'session'):
                        self.invoice_repository.session = db_session
                    self.invoice_repository.update(invoice)
            
            db_session.commit()
            return payment
            
        except Exception as e:
            from infrastructure.databases.session_utils import safe_rollback
            safe_rollback(db_session)
            raise ValueError(f'Error creating payment: {str(e)}')

    def get_payment(self, payment_id: int, household_id: int) -> Optional[Payment]:
        return self.repository.get_by_id(payment_id, household_id)

    def list_payments(self, household_id: int, invoice_id: int = None, customer_id: int = None) -> List[Payment]:
        return self.repository.list(household_id, invoice_id, customer_id)

    def update_payment(self, payment_id: int, household_id: int, method_id: int = None,
                      amount: Decimal = None, description: str = None,
                      updated_by: str = None) -> Payment:
        """
        Update payment (chỉ được update khi status='Draft')
        Cập nhật DebtRecord và AccountingLedger tương ứng
        """
        payment = self.repository.get_by_id(payment_id, household_id)
        if not payment:
            raise ValueError('Payment not found')
        
        if payment.status != 'Draft':
            raise ValueError('Only Draft payments can be updated')
        
        # TODO: Cập nhật DebtRecord và AccountingLedger tương ứng
        # Tạm thời chỉ update payment
        now = datetime.utcnow()
        if method_id is not None:
            payment.method_id = method_id
        if amount is not None:
            payment.amount = amount
        if description is not None:
            payment.description = description
        if updated_by is not None:
            payment.updated_by = updated_by
        payment.updated_at = now
        
        return self.repository.update(payment, household_id)

    def delete_payment(self, payment_id: int, household_id: int) -> None:
        """
        Delete payment (chỉ được delete khi status='Draft')
        Xóa DebtRecord và AccountingLedger tương ứng
        """
        payment = self.repository.get_by_id(payment_id, household_id)
        if not payment:
            raise ValueError('Payment not found')
        
        if payment.status != 'Draft':
            raise ValueError('Only Draft payments can be deleted')
        
        # TODO: Xóa DebtRecord và AccountingLedger tương ứng
        self.repository.delete(payment_id, household_id)

    def _create_debt_record(self, customer_id: int, payment_id: int = None, invoice_id: int = None,
                           debit_amount: Decimal = None, credit_amount: Decimal = None,
                           balance: Decimal = None, description: str = None) -> 'DebtRecord':
        """Helper để tạo DebtRecord domain object"""
        from domain.models.debt_record import DebtRecord
        return DebtRecord(
            id=None,
            customer_id=customer_id,
            invoice_id=invoice_id,
            payment_id=payment_id,
            debit_amount=debit_amount,
            credit_amount=credit_amount,
            balance=balance,
            description=description,
            record_at=datetime.utcnow()
        )

    def _create_accounting_ledger(self, invoice_id: int, transaction_date: datetime,
                                  debit_amount: Decimal = None, credit_amount: Decimal = None,
                                  balance: Decimal = None, description: str = None,
                                  movement_type: str = None) -> 'AccountingLedger':
        """Helper để tạo AccountingLedger domain object"""
        from domain.models.accounting_ledger import AccountingLedger
        return AccountingLedger(
            id=None,
            invoice_id=invoice_id,
            transaction_date=transaction_date,
            description=description,
            debit_amount=debit_amount,
            credit_amount=credit_amount,
            balance=balance,
            document_number="",  # TODO: Generate theo thông tư 88/2021/TT-BTC
            movement_type=movement_type,
            status='Confirm',
            created_at=transaction_date,
            updated_at=transaction_date
        )

    def _get_last_ledger_balance(self, household_id: int) -> Optional['AccountingLedger']:
        """Lấy accounting ledger mới nhất để tính balance"""
        if not self.accounting_ledger_repository:
            return None
        ledgers = self.accounting_ledger_repository.list(household_id)
        return ledgers[0] if ledgers else None
