from marshmallow import Schema, fields

class HouseholdRequestSchema(Schema):
    tax_code = fields.Str(required=False, allow_none=True)
    name = fields.Str(required=False, allow_none=True)
    phone = fields.Str(required=False, allow_none=True)
    address = fields.Str(required=False, allow_none=True)
    description = fields.Str(required=False, allow_none=True)
    status = fields.Str(required=False, allow_none=True)

class HouseholdResponseSchema(Schema):
    id = fields.Int(required=True)
    tax_code = fields.Str(required=False, allow_none=True)
    name = fields.Str(required=False, allow_none=True)
    phone = fields.Str(required=False, allow_none=True)
    address = fields.Str(required=False, allow_none=True)
    description = fields.Str(required=False, allow_none=True)
    status = fields.Str(required=True)
    created_by = fields.Str(required=False, allow_none=True)
    updated_by = fields.Str(required=False, allow_none=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)