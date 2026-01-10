from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Numeric
from infrastructure.databases.base import Base
from datetime import datetime
class SubscriptionPlan(Base):
    __tablename__ = 'subscriptionplans'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    id = Column(Integer, primary_key=True, autoincrement=True) # Cho phép NULL
    name=Column(String(50),nullable=False)
    user_id=Column(Integer, ForeignKey("users.id"),nullable=False) # Role Admin
    billing_cycle=Column(String(50),nullable=True)
    price=Column(Numeric(10), nullable=True)
    description = Column(String(255), nullable=True)
    status = Column(String(50), nullable=False)
    created_by= Column(String(50),nullable=True) # Role Admin
    updated_by= Column(String(50),nullable=True) # Role Admin
    created_at = Column(DateTime,default=datetime.utcnow,nullable=False)
    updated_at = Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow,nullable=False) 
    
    
