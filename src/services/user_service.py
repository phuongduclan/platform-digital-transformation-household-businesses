from domain.models.user import User
from domain.models.iuser_repository import IUserRepository
from typing import List, Optional
from datetime import datetime
from infrastructure.databases.mssql import session
from infrastructure.models import Role

class UserService:
    def __init__(self, repository: IUserRepository):
        self.repository = repository
    
    def _get_role_by_name(self, role_name: str):
        """Lấy Role theo tên (case-insensitive) - Helper method"""
        all_roles = session.query(Role).all()
        return next((r for r in all_roles if r.role_name.upper() == role_name.upper()), None)
    
    def _get_employee_role(self):
        """Lấy Employee role"""
        return self._get_role_by_name('Employee')
    
    def _is_employee_role(self, role_id: int) -> bool:
        """Check role_id có phải Employee không"""
        employee_role = self._get_employee_role()
        return employee_role and role_id == employee_role.id
    
    def _check_admin_cannot_manage_employee(self, user_id: int = None, role_id: int = None, action: str = ""):
        """
        Business rule: Admin không được quản lý Employee
        Raise ValueError nếu vi phạm
        """
        employee_role = self._get_employee_role()
        if not employee_role:
            return
        
        # Check nếu đang cố tạo/update thành Employee
        if role_id and role_id == employee_role.id:
            raise ValueError(f'Admin cannot {action} Employee. Only Owner can manage Employee via /api/owner/employees/')
        
        # Check nếu user hiện tại là Employee
        if user_id:
            existing_user = self.repository.get_by_id(user_id)
            if existing_user and existing_user.role_id == employee_role.id:
                raise ValueError(f'Admin cannot {action} Employee. Only Owner can manage Employee via /api/owner/employees/')

    def create_user(self, household_id: int = None, role_id: int = None, user_name: str = None,
                   password: str = None, email: str = None, description: str = None,
                   status: str = None, created_by: str = None, is_admin_creating: bool = False) -> User:
        """
        Create user với business rules
        
        Args:
            is_admin_creating: True nếu Admin đang tạo (để check business rule)
        """
        # Business rule: Admin không được tạo Employee
        if is_admin_creating:
            self._check_admin_cannot_manage_employee(role_id=role_id, action="create")
        
        from datetime import timezone
        now = datetime.now(timezone.utc)
        user = User(
            id=None, household_id=household_id, role_id=role_id, user_name=user_name,
            password=password, email=email, description=description, status=status,
            created_by=created_by, updated_by=None, created_at=now, updated_at=now
        )
        return self.repository.add(user)

    def get_user(self, user_id: int, is_admin_accessing: bool = False) -> Optional[User]:
        """
        Get user với business rules
        
        Args:
            is_admin_accessing: True nếu Admin đang access (để check business rule)
        """
        user = self.repository.get_by_id(user_id)
        if not user:
            return None
        
        # Business rule: Admin không được xem Employee
        if is_admin_accessing:
            self._check_admin_cannot_manage_employee(user_id=user_id, action="access")
        
        return user

    def list_users(self, exclude_employee: bool = False, role_id: int = None, 
                   status: str = None, household_id: int = None, search_term: str = None) -> List[User]:
        """
        List users với business rules và search/filter
        
        Business Logic: Admin quản lý Owner accounts - view, search, filter, manage
        
        Args:
            exclude_employee: True nếu Admin list (exclude Employee)
            role_id: Filter by role_id (e.g., only Owner - để Admin quản lý Owner accounts)
            status: Filter by status (Active, Inactive) - để activate/deactivate
            household_id: Filter by household_id
            search_term: Search by user_name or email (case-insensitive) - để search Owner accounts
        """
        employee_role = None
        if exclude_employee:
            # Business rule: Admin chỉ quản lý Admin và Owner, KHÔNG Employee
            employee_role = self._get_employee_role()
            if not employee_role:
                # Nếu không tìm thấy Employee role, raise error để đảm bảo business rule
                raise ValueError("Employee role not found in database. Cannot exclude Employee users.")
            
            # BUSINESS RULE VALIDATION: Admin không được filter Employee role
            # Nếu Admin cố filter role_id = Employee, thì phải reject vì conflict
            if role_id is not None and role_id == employee_role.id:
                raise ValueError(f"Admin cannot filter Employee role (role_id={role_id}). Admin can only manage Admin and Owner accounts. Use role_id=1 (Admin) or role_id=2 (Owner).")
        
        # Use search_and_filter if có search_term, filter, hoặc exclude_employee
        if exclude_employee or role_id or status or household_id or search_term:
            return self.repository.search_and_filter(
                exclude_role_id=employee_role.id if employee_role else None,
                role_id=role_id,
                status=status,
                household_id=household_id,
                search_term=search_term
            )
        
        # Default: list all
        return self.repository.list()

    def update_user(self, user_id: int, household_id: int = None, role_id: int = None,
                   user_name: str = None, password: str = None, email: str = None,
                   description: str = None, status: str = None, updated_by: str = None,
                   is_admin_updating: bool = False) -> User:
        """
        Update user với business rules
        
        Args:
            is_admin_updating: True nếu Admin đang update (để check business rule)
        """
        # Business rule: Admin không được update Employee
        if is_admin_updating:
            self._check_admin_cannot_manage_employee(user_id=user_id, role_id=role_id, action="update")
        
        from datetime import timezone
        now = datetime.now(timezone.utc)
        user = User(
            id=user_id, household_id=household_id, role_id=role_id, user_name=user_name,
            password=password, email=email, description=description, status=status,
            updated_by=updated_by, updated_at=now
        )
        return self.repository.update(user)

    def delete_user(self, user_id: int, is_admin_deleting: bool = False) -> None:
        """
        Delete user với business rules
        
        Args:
            is_admin_deleting: True nếu Admin đang delete (để check business rule)
        """
        # Business rule: Admin không được delete Employee
        if is_admin_deleting:
            self._check_admin_cannot_manage_employee(user_id=user_id, action="delete")
        
        self.repository.delete(user_id)

    def get_users_by_household(self, household_id: int) -> List[User]:
        return self.repository.get_by_household_id(household_id)
    
    def list_users_exclude_role(self, exclude_role_id: int) -> List[User]:
        """List all users except users with specific role_id"""
        return self.repository.list_exclude_role(exclude_role_id)
