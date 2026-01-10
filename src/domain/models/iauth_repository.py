from abc import ABC, abstractmethod
from typing import List, Optional
from .user import User

class IAuthRepository(ABC):
    @abstractmethod
    def get_user_by_username(self, username: str) -> Optional[User]:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        pass

    @abstractmethod
    def register(self, user: User) -> Optional[User]:
        pass

    @abstractmethod
    def remember_password(self) -> Optional[User]:
        pass

    @abstractmethod
    def look_account(self, Id: int) -> bool:
        pass

    @abstractmethod
    def un_look_account(self, course_id: int) -> None:
        pass 
    @abstractmethod
    def check_exist(self, username: str) -> bool:
        pass