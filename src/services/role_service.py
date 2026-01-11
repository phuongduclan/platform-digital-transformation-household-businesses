from domain.models.role import Role
from domain.models.irole_repository import IRoleRepository
from typing import List, Optional
from datetime import datetime

class RoleService:
    def __init__(self, repository: IRoleRepository):
        self.repository = repository

    def create_role(self, role_name: str, description: str = None) -> Role:
        now = datetime.utcnow()
        role = Role(id=None, role_name=role_name, description=description,
                   created_at=now, updated_at=now)
        return self.repository.add(role)

    def get_role(self, role_id: int) -> Optional[Role]:
        return self.repository.get_by_id(role_id)

    def list_roles(self) -> List[Role]:
        return self.repository.list()

    def update_role(self, role_id: int, role_name: str = None, description: str = None) -> Role:
        now = datetime.utcnow()
        role = Role(id=role_id, role_name=role_name, description=description, updated_at=now)
        return self.repository.update(role)

    def delete_role(self, role_id: int) -> None:
        self.repository.delete(role_id)
