from abc import ABC, abstractmethod
from .role_function import RoleFunction
from typing import List, Optional

class IRoleFunctionRepository(ABC):
    @abstractmethod
    def add(self, role_function: RoleFunction) -> RoleFunction:
        pass

    @abstractmethod
    def get_by_id(self, role_function_id: int) -> Optional[RoleFunction]:
        pass

    @abstractmethod
    def list(self) -> List[RoleFunction]:
        pass

    @abstractmethod
    def delete(self, role_function_id: int) -> None:
        pass

    @abstractmethod
    def get_by_role_id(self, role_id: int) -> List[RoleFunction]:
        pass

    @abstractmethod
    def get_by_role_and_function(self, role_id: int, function_id: int) -> Optional[RoleFunction]:
        pass
