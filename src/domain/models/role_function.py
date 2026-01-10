class RoleFunction:
    def __init__(self, id: int = None, role_id: int = None, function_id: int = None,
                 created_at = None):
        self.id = id
        self.role_id = role_id
        self.function_id = function_id
        self.created_at = created_at
