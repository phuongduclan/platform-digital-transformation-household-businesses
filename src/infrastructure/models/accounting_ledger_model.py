from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from infrastructure.databases.base import Base
from datetime import datetime
class AccountingLedger(Base):
    __tablename__ = 'accounting_ledger'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    id = Column(Integer, primary_key=True, autoincrement=True) # Cho phép NULL
    invoice_id=Column(Integer, ForeignKey("invoices.id"),nullable=False,unique=True)
    transaction_date= Column(DateTime, nullable=False)
    description = Column(String(255), nullable=False)
    debit_amount=Column(Integer, nullable=True) # Chi
    credit_amount=Column(Integer, nullable=True) # Thu
    balance=Column(Integer, nullable=True)
    document_number=Column(String(50),nullable=False) # Mẫu số theo thông tư 88/2021/TT-BTC
    movement_type=Column(String(50),nullable=False) # Thu / Chi
    status = Column(String(50), nullable=False)
    created_at = Column(DateTime,default=datetime.utcnow,nullable=False)
    updated_at = Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow,nullable=False) 