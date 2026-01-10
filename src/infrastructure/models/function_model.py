from sqlalchemy import Column, Integer, String, DateTime
from infrastructure.databases.base import Base
from datetime import datetime

class Function(Base):
    """
    Function model for RBAC system.
    Defines system functions/permissions that can be assigned to roles.
    Each function represents an API endpoint or group of endpoints with specific HTTP methods.
    """
    __tablename__ = 'functions'
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    function_code = Column(String(20), nullable=False, unique=True)  # F001, F002, F101, etc.
    function_name = Column(String(100), nullable=False)  # manage_households, view_products, etc.
    url_pattern = Column(String(255), nullable=False)  # /api/admin/households/*, /api/products, etc.
    http_methods = Column(String(50), nullable=False)  # C,R,U,D or R or C,R (C=POST, R=GET, U=PUT, D=DELETE)
    description = Column(String(500), nullable=True)
    resource_type = Column(String(50), nullable=True)  # household, product, invoice, etc.
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<Function(id={self.id}, code='{self.function_code}', name='{self.function_name}')>"
    
    def allows_method(self, http_method):
        """
        Check if this function allows a specific HTTP method.
        
        Args:
            http_method: HTTP method string (GET, POST, PUT, DELETE)
            
        Returns:
            bool: True if method is allowed, False otherwise
        """
        method_map = {
            'POST': 'C',
            'GET': 'R',
            'PUT': 'U',
            'PATCH': 'U',
            'DELETE': 'D'
        }
        
        method_code = method_map.get(http_method.upper())
        if not method_code:
            return False
            
        return method_code in self.http_methods
