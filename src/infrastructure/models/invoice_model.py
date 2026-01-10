from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from infrastructure.databases.base import Base
from datetime import datetime

class InvoiceModel(Base):
    """SQLAlchemy model for invoices table"""
    __tablename__ = 'invoices'
    __table_args__ = {'extend_existing': True}
    
    # Common fields
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # From HEAD (Clean Arch features)
    invoice_number = Column(String(50), unique=True, nullable=True) # Set Nullable True to match Main if it doesn't use it yet
    
    # From Main (Business fields)
    household_id = Column(Integer, ForeignKey("households.id"), nullable=False)
    seller_id = Column(Integer, ForeignKey("sellers.id"), nullable=True) # Hóa đơn mua
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=True) # Hóa đơn bán
    invoice_type = Column(String(50), nullable=False, default='SALES')
    discount_total = Column(Numeric(10, 2), nullable=True)
    vat_total = Column(Numeric(10, 2), nullable=False, default=0)
    
    # Hybrid fields
    total_amount = Column(Numeric(10, 2), default=0.0, nullable=False) # Used Numeric from Main
    status = Column(String(50), default='DRAFT', nullable=False)  # DRAFT, CONFIRMED, PAID, CANCELLED
    source = Column(String(20), default='MANUAL', nullable=False)  # MANUAL, AI (From HEAD)
    description = Column(String(255), nullable=True) # From Main
    
    # Audit fields (Hybrid)
    created_by = Column(String(50), nullable=True) # Main uses String username? HEAD used FK to User.
    # HEAD: created_by = Column(Integer, ForeignKey('flask_user.id'), nullable=False)
    # Main: created_by = Column(String(50), nullable=True)
    # Since I kept Main's `users` table, I should probably use Integer ID if I want FK.
    # ALso Main's User table has `created_by` as String.
    # To keep Main compatible, I will use String for now? Or FK to `users.id`?
    # If Main says created_by is string (name), I will stick to Main for now to avoid breaking other things.
    updated_by = Column(String(50), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships (HEAD)
    details = relationship('InvoiceDetailModel', back_populates='invoice', cascade='all, delete-orphan')
    # creator = relationship('UserModel', foreign_keys=[created_by]) # Disable if created_by is String
