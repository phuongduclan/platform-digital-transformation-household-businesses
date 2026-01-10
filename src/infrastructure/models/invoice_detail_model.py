from sqlalchemy import Column, Integer, String, Float, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import relationship
from infrastructure.databases.base import Base
from datetime import datetime

class InvoiceDetailModel(Base):
    """SQLAlchemy model for invoice_details table"""
    __tablename__ = 'invoice_details'
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    invoice_id = Column(Integer, ForeignKey('invoices.id'), nullable=False)
    
    # From Main (Relational)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    unit_id = Column(Integer, ForeignKey("units.id"), nullable=False)
    
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=True) # Main uses price, HEAD used unit_price
    
    # Main extras
    vat = Column(Integer, nullable=False, default=0) # % vat
    discount = Column(Integer, nullable=True, default=0) # % discount
    description = Column(String(255), nullable=True)
    status = Column(String(50), nullable=False, default='ACTIVE')
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    invoice = relationship('InvoiceModel', back_populates='details')
    # product = relationship('Product') # Need Product model import if we want this
