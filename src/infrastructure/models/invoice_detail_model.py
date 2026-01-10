from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.databases.base import Base

class InvoiceDetailModel(Base):
    """SQLAlchemy model for invoice_details table"""
    __tablename__ = 'invoice_details'
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    invoice_id = Column(Integer, ForeignKey('invoices.id'), nullable=False)
    product_name = Column(String(255), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)
    
    # Relationships
    invoice = relationship('InvoiceModel', back_populates='details')
