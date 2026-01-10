from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from infrastructure.databases.base import Base
from datetime import datetime
class ExportDetail(Base):
    __tablename__ = 'export_details'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    id = Column(Integer, primary_key=True, autoincrement=True) # Cho phép NULL
    export_id=Column(Integer,ForeignKey("export_receipts.id"),nullable=False)
    product_id=Column(Integer,ForeignKey("products.id"),nullable=False)
    unit_id=Column(Integer, ForeignKey("units.id"),nullable=False)
    quantity=Column(Integer,nullable=False)
   
