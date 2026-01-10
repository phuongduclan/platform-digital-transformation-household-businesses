from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from infrastructure.databases.base import Base
from datetime import datetime
class ImportDetail(Base):
    __tablename__ = 'import_details'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    id = Column(Integer, primary_key=True, autoincrement=True) # Cho phép NULL
    import_id=Column(Integer,ForeignKey("import_receipts.id"),nullable=False)
    product_id=Column(Integer,ForeignKey("products.id"),nullable=False)
    unit_id=Column(Integer, ForeignKey("units.id"),nullable=False)
    quantity=Column(Integer,nullable=False)
    # Chi tiết nhập kho
   
