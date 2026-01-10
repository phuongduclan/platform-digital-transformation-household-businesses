from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from infrastructure.databases.base import Base
from datetime import datetime
class Inventory(Base):
    __tablename__ = 'inventories'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    id = Column(Integer, primary_key=True, autoincrement=True) # Cho phép NULL
    product_id=Column(Integer,ForeignKey("products.id"),nullable=False)
    unit_id=Column(Integer, ForeignKey("units.id"),nullable=False)
    warehouse_id=Column(Integer, ForeignKey("warehouses.id"),nullable=False)
    quantity=Column(Integer,nullable=False)
    created_at = Column(DateTime,default=datetime.utcnow,nullable=False)
    updated_at = Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow,nullable=False) 
    
   