from marshmallow import Schema, fields

class UserRequestSchema(Schema):
    household_id = fields.Int(required=False, allow_none=True)
    role_id = fields.Int(required=True)
    user_name = fields.Str(required=True)
    password = fields.Str(required=True)
    email = fields.Str(required=False, allow_none=True)
    description = fields.Str(required=False, allow_none=True)
    status = fields.Str(required=True)
    created_by = fields.Str(required=False, allow_none=True)

class UserResponseSchema(Schema):
    id = fields.Int(required=True)
    household_id = fields.Int(required=False, allow_none=True)
    role_id = fields.Int(required=True)
    user_name = fields.Str(required=True)
    email = fields.Str(required=False, allow_none=True)
    description = fields.Str(required=False, allow_none=True)
    status = fields.Str(required=True)
    created_by = fields.Str(required=False, allow_none=True)
    updated_by = fields.Str(required=False, allow_none=True)
    created_at = fields.Raw(required=True)
    updated_at = fields.Raw(required=True)

class UserUpdateSchema(Schema):
    household_id = fields.Int(required=False, allow_none=True)
    role_id = fields.Int(required=False)
    user_name = fields.Str(required=False)
    password = fields.Str(required=False)
    email = fields.Str(required=False, allow_none=True)
    description = fields.Str(required=False, allow_none=True)
    status = fields.Str(required=False)
    updated_by = fields.Str(required=False, allow_none=True)
