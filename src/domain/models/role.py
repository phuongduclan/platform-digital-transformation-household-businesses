class Role:
    def __init__(self, id: int = None, role_name: str = None, description: str = None,
                 created_at = None, updated_at = None):
        self.id = id
        self.role_name = role_name
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at
