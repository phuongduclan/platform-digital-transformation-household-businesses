from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Numeric
from infrastructure.databases.base import Base
from datetime import datetime
class InvoiceDetailModel(Base):
    __tablename__ = 'invoice_details'
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    invoice_id = Column(Integer, ForeignKey('invoices.id'), nullable=False)
    
    # Financial fields
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    unit_id = Column(Integer, ForeignKey("units.id"), nullable=True)
    product_name = Column(String(255), nullable=True) # Supports free-text products
    
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=True) # Main's field name
    unit_price = Column(Numeric(10, 2), nullable=True) # HEAD's field name, keep for compatibility
    subtotal = Column(Numeric(10, 2), nullable=True)
    
    vat = Column(Integer, nullable=False, default=0) # % vat
    discount = Column(Integer, nullable=True, default=0) # % discount
    description = Column(String(255), nullable=True)
    quantity=Column(Integer,nullable=False)
    status = Column(String(50), nullable=False)  # Draft / Confirm / Delete 
    created_at = Column(DateTime,default=datetime.utcnow,nullable=False)
    updated_at = Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow,nullable=False) 
