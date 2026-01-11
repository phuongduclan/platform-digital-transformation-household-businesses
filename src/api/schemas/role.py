from marshmallow import Schema, fields

class RoleRequestSchema(Schema):
    role_name = fields.Str(required=True)
    description = fields.Str(required=False, allow_none=True)

class RoleResponseSchema(Schema):
    id = fields.Int(required=True)
    role_name = fields.Str(required=True)
    description = fields.Str(required=False, allow_none=True)
    created_at = fields.Raw(required=True)
    updated_at = fields.Raw(required=True)

class RoleUpdateSchema(Schema):
    role_name = fields.Str(required=False)
    description = fields.Str(required=False, allow_none=True)
