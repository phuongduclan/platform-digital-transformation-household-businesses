from abc import ABC, abstractmethod
from domain.models.todo import Todo
from typing import List, Optional

class ITodoService(ABC):
    @abstractmethod
    def create_todo(self, title: str, description: str, status: str, created_at, updated_at) -> Todo:
        pass

    @abstractmethod
    def get_todo(self, todo_id: int) -> Optional[Todo]:
        pass

    @abstractmethod
    def list_todos(self) -> List[Todo]:
        pass

    @abstractmethod
    def update_todo(self, todo_id: int, title: str, description: str, status: str, created_at, updated_at) -> Todo:
        pass

    @abstractmethod
    def delete_todo(self, todo_id: int) -> None:
        pass
