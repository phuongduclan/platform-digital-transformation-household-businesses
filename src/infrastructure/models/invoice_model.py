from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Numeric
from infrastructure.databases.base import Base
from datetime import datetime
class InvoiceModel(Base):
    __tablename__ = 'invoices'
    __table_args__ = {'extend_existing': True}
    
    # Common fields
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # New fields
    invoice_number = Column(String(50), unique=True, nullable=True) 
    customer_name = Column(String(255), nullable=True) 
    
    # Relational & Business fields
    household_id = Column(Integer, ForeignKey("households.id"), nullable=False)
    seller_id = Column(Integer, ForeignKey("sellers.id"), nullable=True) # Hóa đơn mua
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True) # Hóa đơn bán
    invoice_type = Column(String(50), nullable=False, default='SALES')
    
    discount_total = Column(Numeric(10, 2), nullable=True, default=0.0)
    vat_total = Column(Numeric(10, 2), nullable=False, default=0.0)
    total_amount = Column(Numeric(10, 2), default=0.0, nullable=False)
    
    status = Column(String(50), default='DRAFT', nullable=False)  # DRAFT, CONFIRMED, PAID, CANCELLED
    source = Column(String(20), default='MANUAL', nullable=False)  # MANUAL, AI
    description = Column(String(255), nullable=True) 
    
    # Audit fields
    created_by = Column(String(50), nullable=True) 
    updated_by = Column(String(50), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    from sqlalchemy.orm import relationship
    details = relationship('InvoiceDetail', backref='invoice', cascade='all, delete-orphan')
