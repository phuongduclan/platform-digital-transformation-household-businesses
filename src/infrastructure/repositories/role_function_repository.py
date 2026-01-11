from domain.models.irole_function_repository import IRoleFunctionRepository
from domain.models.role_function import RoleFunction
from typing import List, Optional
from infrastructure.models import RoleFunction as RoleFunctionModel
from infrastructure.databases.mssql import session

class RoleFunctionRepository(IRoleFunctionRepository):
    def __init__(self, session=session):
        self.session = session

    def add(self, role_function: RoleFunction) -> RoleFunctionModel:
        try:
            role_function_model = RoleFunctionModel(
                role_id=role_function.role_id,
                function_id=role_function.function_id,
                created_at=role_function.created_at
            )
            self.session.add(role_function_model)
            self.session.commit()
            self.session.refresh(role_function_model)
            return role_function_model
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error creating role_function: {str(e)}')

    def get_by_id(self, role_function_id: int) -> Optional[RoleFunctionModel]:
        return self.session.query(RoleFunctionModel).filter_by(id=role_function_id).first()

    def list(self) -> List[RoleFunctionModel]:
        return self.session.query(RoleFunctionModel).all()

    def delete(self, role_function_id: int) -> None:
        try:
            role_function = self.session.query(RoleFunctionModel).filter_by(id=role_function_id).first()
            if role_function:
                self.session.delete(role_function)
                self.session.commit()
            else:
                raise ValueError('RoleFunction not found')
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error deleting role_function: {str(e)}')

    def get_by_role_id(self, role_id: int) -> List[RoleFunctionModel]:
        return self.session.query(RoleFunctionModel).filter_by(role_id=role_id).all()

    def get_by_role_and_function(self, role_id: int, function_id: int) -> Optional[RoleFunctionModel]:
        return self.session.query(RoleFunctionModel).filter_by(
            role_id=role_id, function_id=function_id
        ).first()
