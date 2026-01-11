from marshmallow import Schema, fields

class FunctionRequestSchema(Schema):
    function_code = fields.Str(required=True)
    function_name = fields.Str(required=True)
    url_pattern = fields.Str(required=True)
    http_methods = fields.Str(required=True)
    description = fields.Str(required=False, allow_none=True)
    resource_type = fields.Str(required=False, allow_none=True)

class FunctionResponseSchema(Schema):
    id = fields.Int(required=True)
    function_code = fields.Str(required=True)
    function_name = fields.Str(required=True)
    url_pattern = fields.Str(required=True)
    http_methods = fields.Str(required=True)
    description = fields.Str(required=False, allow_none=True)
    resource_type = fields.Str(required=False, allow_none=True)
    created_at = fields.Raw(required=True)
    updated_at = fields.Raw(required=True)

class FunctionUpdateSchema(Schema):
    function_code = fields.Str(required=False)
    function_name = fields.Str(required=False)
    url_pattern = fields.Str(required=False)
    http_methods = fields.Str(required=False)
    description = fields.Str(required=False, allow_none=True)
    resource_type = fields.Str(required=False, allow_none=True)
