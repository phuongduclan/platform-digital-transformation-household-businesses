"""
Permission Service - Check role có function code không
"""
from infrastructure.databases.mssql import session
from infrastructure.models import RoleFunction, Function, Role

class PermissionService:
    def __init__(self, db_session):
        self.session = db_session
    
    def check_role_has_function(self, role_id, function_code, http_method):
        """
        Check role có function code và HTTP method phù hợp không
        
        Args:
            role_id: ID của role
            function_code: Code của function (F001, F101, etc.)
            http_method: HTTP method (GET, POST, PUT, DELETE)
            
        Returns:
            bool: True nếu có permission, False nếu không
        """
        # Tìm function theo code
        function = self.session.query(Function).filter_by(function_code=function_code).first()
        if not function:
            return False
        
        # Check role có function này không
        role_function = self.session.query(RoleFunction).filter_by(
            role_id=role_id,
            function_id=function.id
        ).first()
        
        if not role_function:
            return False
        
        # Check HTTP method có trong function.http_methods không
        return function.allows_method(http_method)
    
    def get_role_functions(self, role_id):
        """Lấy tất cả functions của role"""
        role_functions = self.session.query(RoleFunction).filter_by(role_id=role_id).all()
        function_ids = [rf.function_id for rf in role_functions]
        functions = self.session.query(Function).filter(Function.id.in_(function_ids)).all()
        return functions
