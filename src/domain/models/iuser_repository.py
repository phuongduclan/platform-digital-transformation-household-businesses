from abc import ABC, abstractmethod
from .user import User
from typing import List, Optional

class IUserRepository(ABC):
    @abstractmethod
    def add(self, user: User) -> User:
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def list(self) -> List[User]:
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        pass

    @abstractmethod
    def delete(self, user_id: int) -> None:
        pass

    @abstractmethod
    def get_by_household_id(self, household_id: int) -> List[User]:
        pass
    
    @abstractmethod
    def list_exclude_role(self, exclude_role_id: int) -> List[User]:
        pass
    
    @abstractmethod
    def search_and_filter(self, exclude_role_id: int = None, role_id: int = None, 
                         status: str = None, household_id: int = None,
                         search_term: str = None) -> List[User]:
        """
        Search and filter users
        
        Args:
            exclude_role_id: Exclude users with this role_id (e.g., exclude Employee)
            role_id: Filter by role_id (e.g., only Owner)
            status: Filter by status (Active, Inactive)
            household_id: Filter by household_id
            search_term: Search by user_name or email (case-insensitive, partial match)
        """
        pass
