from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Numeric
from infrastructure.databases.base import Base
from datetime import datetime
class DebtRecord(Base):
    __tablename__ = 'debt_record'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    id = Column(Integer, primary_key=True, autoincrement=True) # Cho phép NULL
    customer_id=Column(Integer, ForeignKey("customers.id"),nullable=False)
    invoice_id=Column(Integer, ForeignKey("invoices.id"),nullable=True,unique=True) # Mã chứng từ hóa đơn nợ
    payment_id=Column(Integer, ForeignKey("payments.id"),nullable=True,unique=True) # Mã chứng từ thanh toán trả nợ
    debit_amount=Column(Numeric(10), nullable=True) # nợ
    credit_amount=Column(Numeric(10), nullable=True)  # trả
    balance=Column(Numeric(10), nullable=True)  # trả - nợ
    description = Column(String(255), nullable=True) # Diễn giải
    record_at = Column(DateTime,default=datetime.utcnow,nullable=False)
    
    
