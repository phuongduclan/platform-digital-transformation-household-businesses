from domain.models.ifunction_repository import IFunctionRepository
from domain.models.function import Function
from typing import List, Optional
from infrastructure.models import Function as FunctionModel
from infrastructure.databases.mssql import session

class FunctionRepository(IFunctionRepository):
    def __init__(self, session=session):
        self.session = session

    def add(self, function: Function) -> FunctionModel:
        try:
            function_model = FunctionModel(
                function_code=function.function_code,
                function_name=function.function_name,
                url_pattern=function.url_pattern,
                http_methods=function.http_methods,
                description=function.description,
                resource_type=function.resource_type,
                created_at=function.created_at,
                updated_at=function.updated_at
            )
            self.session.add(function_model)
            self.session.commit()
            self.session.refresh(function_model)
            return function_model
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error creating function: {str(e)}')

    def get_by_id(self, function_id: int) -> Optional[FunctionModel]:
        return self.session.query(FunctionModel).filter_by(id=function_id).first()

    def list(self) -> List[FunctionModel]:
        return self.session.query(FunctionModel).all()

    def update(self, function: Function) -> FunctionModel:
        try:
            function_model = self.session.query(FunctionModel).filter_by(id=function.id).first()
            if not function_model:
                raise ValueError('Function not found')
            
            if function.function_code is not None:
                function_model.function_code = function.function_code
            if function.function_name is not None:
                function_model.function_name = function.function_name
            if function.url_pattern is not None:
                function_model.url_pattern = function.url_pattern
            if function.http_methods is not None:
                function_model.http_methods = function.http_methods
            if function.description is not None:
                function_model.description = function.description
            if function.resource_type is not None:
                function_model.resource_type = function.resource_type
            if function.updated_at is not None:
                function_model.updated_at = function.updated_at
            
            self.session.commit()
            self.session.refresh(function_model)
            return function_model
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error updating function: {str(e)}')

    def delete(self, function_id: int) -> None:
        try:
            function = self.session.query(FunctionModel).filter_by(id=function_id).first()
            if function:
                self.session.delete(function)
                self.session.commit()
            else:
                raise ValueError('Function not found')
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error deleting function: {str(e)}')

    def get_by_code(self, function_code: str) -> Optional[FunctionModel]:
        return self.session.query(FunctionModel).filter_by(function_code=function_code).first()
