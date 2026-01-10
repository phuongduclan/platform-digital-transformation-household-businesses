from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from infrastructure.databases.base import Base
from datetime import datetime
class PaymentMethod(Base):
    __tablename__ = 'paymentmethods'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    id = Column(Integer, primary_key=True, autoincrement=True) # Cho phép NULL
    name =Column(String(50),nullable=True)
    status = Column(String(50), nullable=False)
    created_at = Column(DateTime,default=datetime.utcnow,nullable=False)
    updated_at = Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow,nullable=False) 
    