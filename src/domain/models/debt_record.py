from datetime import datetime
from decimal import Decimal
from typing import Optional

class DebtRecord:
    def __init__(self, id: int = None, customer_id: int = None, invoice_id: int = None,
                 payment_id: int = None, debit_amount: Decimal = None, credit_amount: Decimal = None,
                 balance: Decimal = None, description: str = None, record_at: datetime = None):
        self.id = id
        self.customer_id = customer_id
        self.invoice_id = invoice_id  # null nếu là bản ghi trả
        self.payment_id = payment_id  # null nếu là bản ghi nợ
        self.debit_amount = debit_amount  # nợ
        self.credit_amount = credit_amount  # trả
        self.balance = balance  # số dư tích lũy
        self.description = description
        self.record_at = record_at
