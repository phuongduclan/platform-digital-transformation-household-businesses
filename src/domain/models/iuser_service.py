from abc import ABC, abstractmethod
from domain.models.user import User
from typing import List, Optional

class IUserService(ABC):
    @abstractmethod
    def create_user(self, household_id: int = None, role_id: int = None, user_name: str = None,
                   password: str = None, email: str = None, description: str = None,
                   status: str = None, created_by: str = None, is_admin_creating: bool = False) -> User:
        pass

    @abstractmethod
    def get_user(self, user_id: int, is_admin_accessing: bool = False) -> Optional[User]:
        pass

    @abstractmethod
    def list_users(self, exclude_employee: bool = False, role_id: int = None, 
                   status: str = None, household_id: int = None, search_term: str = None) -> List[User]:
        pass

    @abstractmethod
    def update_user(self, user_id: int, household_id: int = None, role_id: int = None,
                   user_name: str = None, password: str = None, email: str = None,
                   description: str = None, status: str = None, updated_by: str = None,
                   is_admin_updating: bool = False) -> User:
        pass

    @abstractmethod
    def delete_user(self, user_id: int, is_admin_deleting: bool = False) -> None:
        pass

    @abstractmethod
    def get_users_by_household(self, household_id: int) -> List[User]:
        pass

    @abstractmethod
    def list_users_exclude_role(self, exclude_role_id: int) -> List[User]:
        pass
