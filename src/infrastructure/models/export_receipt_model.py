from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Date
from infrastructure.databases.base import Base
from datetime import datetime

class ExportReceipt(Base):
    __tablename__ = 'export_receipts'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True) # Cho phép NULL
    warehouse_id=Column(Integer, ForeignKey("warehouses.id"),nullable=False)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=True)
    created_at = Column(DateTime,default=datetime.utcnow,nullable=False)
    export_date=Column(Date,nullable=False )
    reason=Column(String(50),nullable=False)
    updated_at = Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow,nullable=False)