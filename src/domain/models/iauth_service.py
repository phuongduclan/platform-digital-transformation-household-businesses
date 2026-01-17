from abc import ABC, abstractmethod
from typing import Optional, Dict

class IAuthService(ABC):
    @abstractmethod
    def authenticate_user(self, user_name: str, password: str):
        """Authenticate user với business rules"""
        pass

    @abstractmethod
    def generate_jwt_token(self, user) -> str:
        """Generate JWT token với đầy đủ thông tin"""
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: int):
        """Get user by id"""
        pass

    @abstractmethod
    def decode_token(self, token: str) -> Dict:
        """Decode JWT token"""
        pass
