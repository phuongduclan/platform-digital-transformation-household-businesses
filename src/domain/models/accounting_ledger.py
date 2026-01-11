from datetime import datetime
from decimal import Decimal
from typing import Optional

class AccountingLedger:
    def __init__(self, id: int = None, invoice_id: int = None, transaction_date: datetime = None,
                 description: str = None, debit_amount: Decimal = None, credit_amount: Decimal = None,
                 balance: Decimal = None, document_number: str = None, movement_type: str = None,
                 status: str = None, created_at: datetime = None, updated_at: datetime = None):
        self.id = id
        self.invoice_id = invoice_id
        self.transaction_date = transaction_date
        self.description = description
        self.debit_amount = debit_amount  # Chi
        self.credit_amount = credit_amount  # Thu
        self.balance = balance  # số dư tài khoản tích lũy
        self.document_number = document_number  # Mẫu số theo thông tư 88/2021/TT-BTC
        self.movement_type = movement_type  # Thu / Chi
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
