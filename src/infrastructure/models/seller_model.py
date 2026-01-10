from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from infrastructure.databases.base import Base
from datetime import datetime
class Seller(Base):
    __tablename__ = 'sellers'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    id = Column(Integer, primary_key=True, autoincrement=True) # Cho phép NULL
    household_id= Column(Integer, ForeignKey("households.id"),nullable=False)
    tax_code=Column(String(12),nullable=True,unique=True) # Mã số thuế hộ kinh doanh bằng số CCCD người đại diện
    name =Column(String(50),nullable=True)
    phone =Column(String(20),nullable=True)
    address =Column(String(255),nullable=True)
    description = Column(String(255), nullable=True)
    status = Column(String(50), nullable=False)
    created_by= Column(String(50),nullable=True)
    updated_by= Column(String(50),nullable=True)
    created_at = Column(DateTime,default=datetime.utcnow,nullable=False)
    updated_at = Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow,nullable=False)
   
    

