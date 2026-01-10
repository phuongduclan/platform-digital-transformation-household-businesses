from domain.models.function import Function
from domain.models.ifunction_repository import IFunctionRepository
from typing import List, Optional
from datetime import datetime

class FunctionService:
    def __init__(self, repository: IFunctionRepository):
        self.repository = repository

    def create_function(self, function_code: str, function_name: str, url_pattern: str,
                       http_methods: str, description: str = None, resource_type: str = None) -> Function:
        now = datetime.utcnow()
        function = Function(
            id=None, function_code=function_code, function_name=function_name,
            url_pattern=url_pattern, http_methods=http_methods, description=description,
            resource_type=resource_type, created_at=now, updated_at=now
        )
        return self.repository.add(function)

    def get_function(self, function_id: int) -> Optional[Function]:
        return self.repository.get_by_id(function_id)

    def list_functions(self) -> List[Function]:
        return self.repository.list()

    def update_function(self, function_id: int, function_code: str = None, function_name: str = None,
                       url_pattern: str = None, http_methods: str = None, description: str = None,
                       resource_type: str = None) -> Function:
        now = datetime.utcnow()
        function = Function(
            id=function_id, function_code=function_code, function_name=function_name,
            url_pattern=url_pattern, http_methods=http_methods, description=description,
            resource_type=resource_type, updated_at=now
        )
        return self.repository.update(function)

    def delete_function(self, function_id: int) -> None:
        self.repository.delete(function_id)

    def get_function_by_code(self, function_code: str) -> Optional[Function]:
        return self.repository.get_by_code(function_code)
