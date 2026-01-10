from abc import ABC, abstractmethod
from .role import Role
from typing import List, Optional

class IRoleRepository(ABC):
    @abstractmethod
    def add(self, role: Role) -> Role:
        pass

    @abstractmethod
    def get_by_id(self, role_id: int) -> Optional[Role]:
        pass

    @abstractmethod
    def list(self) -> List[Role]:
        pass

    @abstractmethod
    def update(self, role: Role) -> Role:
        pass

    @abstractmethod
    def delete(self, role_id: int) -> None:
        pass
