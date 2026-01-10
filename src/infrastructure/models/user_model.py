from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from infrastructure.databases.base import Base
from datetime import datetime

class UserModel(Base):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    household_id = Column(Integer, ForeignKey("households.id"), nullable=True)  # NULL for Admin
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)  # FK to roles table
    username = Column(String(18), nullable=False, unique=True) # Mapped to user_name in Service if needed, or keep username
    password = Column(String(255), nullable=False)  # Increased length for hashed passwords
    email = Column(String(100), nullable=True, unique=True)
    description = Column(String(255), nullable=True)
    status = Column(String(50), nullable=False, default='ACTIVE')
    created_by = Column(String(50), nullable=True)  # Role Admin or Owner
    updated_by = Column(String(50), nullable=True)  # Role Admin or Owner
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', role_id={self.role_id})>"