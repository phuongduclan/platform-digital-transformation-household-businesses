from abc import ABC, abstractmethod
from .function import Function
from typing import List, Optional

class IFunctionRepository(ABC):
    @abstractmethod
    def add(self, function: Function) -> Function:
        pass

    @abstractmethod
    def get_by_id(self, function_id: int) -> Optional[Function]:
        pass

    @abstractmethod
    def list(self) -> List[Function]:
        pass

    @abstractmethod
    def update(self, function: Function) -> Function:
        pass

    @abstractmethod
    def delete(self, function_id: int) -> None:
        pass

    @abstractmethod
    def get_by_code(self, function_code: str) -> Optional[Function]:
        pass
