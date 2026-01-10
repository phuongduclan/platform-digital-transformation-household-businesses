from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Boolean
from infrastructure.databases.base import Base
from datetime import datetime
class Subscription(Base):
    __tablename__ = 'subscriptions'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    id = Column(Integer, primary_key=True, autoincrement=True) # Cho phép NULL
    plan_id=Column(Integer,ForeignKey("subscriptionplans.id"),nullable=False)
    household_id= Column(Integer, ForeignKey("households.id"),nullable=False)
    start_date=Column(DateTime,nullable=False )
    end_date=Column(DateTime,nullable= False)
    is_active = Column(Boolean, nullable=False)
    created_at = Column(DateTime,default=datetime.utcnow,nullable=False)
    updated_at = Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow,nullable=False)
    
    
