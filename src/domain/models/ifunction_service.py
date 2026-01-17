from abc import ABC, abstractmethod
from domain.models.function import Function
from typing import List, Optional

class IFunctionService(ABC):
    @abstractmethod
    def create_function(self, function_code: str, function_name: str, url_pattern: str,
                       http_methods: str, description: str = None, resource_type: str = None) -> Function:
        pass

    @abstractmethod
    def get_function(self, function_id: int) -> Optional[Function]:
        pass

    @abstractmethod
    def list_functions(self) -> List[Function]:
        pass

    @abstractmethod
    def update_function(self, function_id: int, function_code: str = None, function_name: str = None,
                       url_pattern: str = None, http_methods: str = None, description: str = None,
                       resource_type: str = None) -> Function:
        pass

    @abstractmethod
    def delete_function(self, function_id: int) -> None:
        pass

    @abstractmethod
    def get_function_by_code(self, function_code: str) -> Optional[Function]:
        pass
