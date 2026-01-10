from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from infrastructure.databases.base import Base
from datetime import datetime

class RoleFunction(Base):
    """
    RoleFunction model - Junction table for many-to-many relationship between Roles and Functions.
    Maps which functions (permissions) are assigned to which roles.
    """
    __tablename__ = 'role_functions'
    __table_args__ = (
        UniqueConstraint('role_id', 'function_id', name='uq_role_function'),
        {'extend_existing': True}
    )
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    role_id = Column(Integer, ForeignKey('roles.id', ondelete='CASCADE'), nullable=False)
    function_id = Column(Integer, ForeignKey('functions.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<RoleFunction(role_id={self.role_id}, function_id={self.function_id})>"
