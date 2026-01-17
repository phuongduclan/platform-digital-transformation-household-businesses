from abc import ABC, abstractmethod
from domain.models.role_function import RoleFunction
from typing import List, Optional

class IRoleFunctionService(ABC):
    @abstractmethod
    def assign_function_to_role(self, role_id: int, function_id: int) -> RoleFunction:
        pass

    @abstractmethod
    def get_role_function(self, role_function_id: int) -> Optional[RoleFunction]:
        pass

    @abstractmethod
    def list_role_functions(self) -> List[RoleFunction]:
        pass

    @abstractmethod
    def get_functions_by_role(self, role_id: int) -> List[RoleFunction]:
        pass

    @abstractmethod
    def remove_function_from_role(self, role_id: int, function_id: int) -> None:
        pass
