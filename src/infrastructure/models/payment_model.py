from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Numeric
from infrastructure.databases.base import Base
from datetime import datetime
class Payment(Base):
    __tablename__ = 'payments'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    id = Column(Integer, primary_key=True, autoincrement=True) # Cho phép NULL
    invoice_id=Column(Integer, ForeignKey("invoices.id"),nullable=False)
    method_id=Column(Integer,ForeignKey("paymentmethods.id"),nullable=False)
    amount=Column(Numeric(10), nullable=False)
    description = Column(String(255), nullable=True)
    status = Column(String(50), nullable=False)
    created_by= Column(String(50),nullable=True)
    updated_by= Column(String(50),nullable=True)
    created_at = Column(DateTime,default=datetime.utcnow,nullable=False)
    updated_at = Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow,nullable=False) 
   
   