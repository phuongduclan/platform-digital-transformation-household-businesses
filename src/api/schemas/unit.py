from marshmallow import Schema, fields, validate

class UnitRequestSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=False, allow_none=True)
    status = fields.Str(
        required=False,
        validate=validate.OneOf(["ACTIVE", "INACTIVE"]),
        load_default="ACTIVE"
    )

class UnitUpdateSchema(Schema):
    name = fields.Str(required=False)
    description = fields.Str(required=False, allow_none=True)
    status = fields.Str(
        required=False,
        validate=validate.OneOf(["ACTIVE", "INACTIVE"])
    )

class UnitResponseSchema(Schema):
    id = fields.Int(required=True)
    household_id = fields.Int(required=True)
    name = fields.Str(required=True)
    description = fields.Str(required=False, allow_none=True)
    status = fields.Str(required=True)
    created_at = fields.Raw(required=True)
    updated_at = fields.Raw(required=True)