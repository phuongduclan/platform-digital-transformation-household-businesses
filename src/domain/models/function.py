class Function:
    def __init__(self, id: int = None, function_code: str = None, function_name: str = None,
                 url_pattern: str = None, http_methods: str = None, description: str = None,
                 resource_type: str = None, created_at = None, updated_at = None):
        self.id = id
        self.function_code = function_code
        self.function_name = function_name
        self.url_pattern = url_pattern
        self.http_methods = http_methods
        self.description = description
        self.resource_type = resource_type
        self.created_at = created_at
        self.updated_at = updated_at
