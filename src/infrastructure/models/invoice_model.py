from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.databases.base import Base

class InvoiceModel(Base):
    """SQLAlchemy model for invoices table"""
    __tablename__ = 'invoices'
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    invoice_number = Column(String(50), unique=True, nullable=False)
    customer_name = Column(String(255), nullable=False)
    total_amount = Column(Float, default=0.0, nullable=False)
    status = Column(String(20), default='DRAFT', nullable=False)  # DRAFT, CONFIRMED, PAID, CANCELLED
    source = Column(String(20), default='MANUAL', nullable=False)  # MANUAL, AI
    created_by = Column(Integer, ForeignKey('flask_user.id'), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    
    # Relationships
    details = relationship('InvoiceDetailModel', back_populates='invoice', cascade='all, delete-orphan')
    creator = relationship('UserModel', foreign_keys=[created_by])
