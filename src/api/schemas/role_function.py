from marshmallow import Schema, fields

class RoleFunctionRequestSchema(Schema):
    function_id = fields.Int(required=True)

class RoleFunctionResponseSchema(Schema):
    id = fields.Int(required=True)
    role_id = fields.Int(required=True)
    function_id = fields.Int(required=True)
    created_at = fields.Raw(required=True)
