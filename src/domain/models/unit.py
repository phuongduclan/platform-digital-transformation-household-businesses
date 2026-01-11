class Unit:
    def __init__(self, id: int = None, household_id: int = None, 
                 name: str = None, description: str = None, status: str = None,
                 created_at = None, updated_at = None):
        self.id = id
        self.household_id = household_id
        self.name = name
        self.description = description
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at