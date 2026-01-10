from sqlalchemy import Column, Integer, String, DateTime
from infrastructure.databases.base import Base
from datetime import datetime

class Role(Base):
    """
    Role model for RBAC system.
    Defines the three main roles: Admin, Owner, Employee
    """
    __tablename__ = 'roles'
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(String(50), nullable=False, unique=True)  # Admin, Owner, Employee
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<Role(id={self.id}, role_name='{self.role_name}')>"
