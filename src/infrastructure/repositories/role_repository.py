from domain.models.irole_repository import IRoleRepository
from domain.models.role import Role
from typing import List, Optional
from infrastructure.models import Role as RoleModel
from infrastructure.databases.mssql import session

class RoleRepository(IRoleRepository):
    def __init__(self, session=session):
        self.session = session

    def add(self, role: Role) -> RoleModel:
        try:
            role_model = RoleModel(
                role_name=role.role_name,
                description=role.description,
                created_at=role.created_at,
                updated_at=role.updated_at
            )
            self.session.add(role_model)
            self.session.commit()
            self.session.refresh(role_model)
            return role_model
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error creating role: {str(e)}')

    def get_by_id(self, role_id: int) -> Optional[RoleModel]:
        return self.session.query(RoleModel).filter_by(id=role_id).first()

    def list(self) -> List[RoleModel]:
        return self.session.query(RoleModel).all()

    def update(self, role: Role) -> RoleModel:
        try:
            role_model = self.session.query(RoleModel).filter_by(id=role.id).first()
            if not role_model:
                raise ValueError('Role not found')
            
            if role.role_name is not None:
                role_model.role_name = role.role_name
            if role.description is not None:
                role_model.description = role.description
            if role.updated_at is not None:
                role_model.updated_at = role.updated_at
            
            self.session.commit()
            self.session.refresh(role_model)
            return role_model
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error updating role: {str(e)}')

    def delete(self, role_id: int) -> None:
        try:
            role = self.session.query(RoleModel).filter_by(id=role_id).first()
            if role:
                self.session.delete(role)
                self.session.commit()
            else:
                raise ValueError('Role not found')
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error deleting role: {str(e)}')
