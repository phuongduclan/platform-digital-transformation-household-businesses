from abc import ABC, abstractmethod
from typing import List

class IPermissionService(ABC):
    @abstractmethod
    def check_role_has_function(self, role_id, function_code, http_method) -> bool:
        """Check role có function code và HTTP method phù hợp không"""
        pass

    @abstractmethod
    def get_role_functions(self, role_id) -> List:
        """Lấy tất cả functions của role"""
        pass
