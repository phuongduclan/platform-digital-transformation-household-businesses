from domain.models.role_function import RoleFunction
from domain.models.irole_function_repository import IRoleFunctionRepository
from typing import List, Optional
from datetime import datetime

class RoleFunctionService:
    def __init__(self, repository: IRoleFunctionRepository):
        self.repository = repository

    def assign_function_to_role(self, role_id: int, function_id: int) -> RoleFunction:
        now = datetime.utcnow()
        role_function = RoleFunction(
            id=None, role_id=role_id, function_id=function_id, created_at=now
        )
        return self.repository.add(role_function)

    def get_role_function(self, role_function_id: int) -> Optional[RoleFunction]:
        return self.repository.get_by_id(role_function_id)

    def list_role_functions(self) -> List[RoleFunction]:
        return self.repository.list()

    def get_functions_by_role(self, role_id: int) -> List[RoleFunction]:
        return self.repository.get_by_role_id(role_id)

    def remove_function_from_role(self, role_id: int, function_id: int) -> None:
        role_function = self.repository.get_by_role_and_function(role_id, function_id)
        if role_function:
            self.repository.delete(role_function.id)
