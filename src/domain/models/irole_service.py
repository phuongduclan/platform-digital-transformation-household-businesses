from abc import ABC, abstractmethod
from domain.models.role import Role
from typing import List, Optional
from datetime import datetime

class IRoleService(ABC):
    @abstractmethod
    def create_role(self, role_name: str, description: str = None) -> Role:
        pass

    @abstractmethod
    def get_role(self, role_id: int) -> Optional[Role]:
        pass

    @abstractmethod
    def list_roles(self) -> List[Role]:
        pass

    @abstractmethod
    def update_role(self, role_id: int, role_name: str = None, description: str = None) -> Role:
        pass

    @abstractmethod
    def delete_role(self, role_id: int) -> None:
        pass
