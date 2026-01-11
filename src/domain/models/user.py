class User:
    def __init__(self, id: int = None, household_id: int = None, role_id: int = None, 
                 user_name: str = None, password: str = None, email: str = None,
                 description: str = None, status: str = None, created_by: str = None,
                 updated_by: str = None, created_at = None, updated_at = None):
        self.id = id
        self.household_id = household_id
        self.role_id = role_id
        self.user_name = user_name
        self.password = password
        self.email = email
        self.description = description
        self.status = status
        self.created_by = created_by
        self.updated_by = updated_by
        self.created_at = created_at
        self.updated_at = updated_at
