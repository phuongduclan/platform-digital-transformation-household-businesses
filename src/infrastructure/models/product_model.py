from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from infrastructure.databases.base import Base
from datetime import datetime
class Product(Base):
    __tablename__ = 'products'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    id = Column(Integer, primary_key=True, autoincrement=True) # Cho phép NULL
    household_id=Column(Integer, ForeignKey("households.id"),nullable=False)
    category_id=Column(Integer,ForeignKey("categories.id"),nullable=False)
    name =Column(String(50),nullable=True)
    image_url=Column(String(255),nullable=True)
    description = Column(String(255), nullable=True)
    status = Column(String(50), nullable=False)
    created_at = Column(DateTime,default=datetime.utcnow,nullable=False)
    updated_at = Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow,nullable=False) 
  
    
