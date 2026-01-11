from marshmallow import Schema, fields, validate


class WarehouseRequestSchema(Schema):
    name = fields.Str(required=True)
    address = fields.Str(required=True)
    description = fields.Str(required=False, allow_none=True)
    status = fields.Str(
        required=False,
        validate=validate.OneOf(["ACTIVE", "INACTIVE"]),
        load_default="ACTIVE"
    )

class WarehouseUpdateSchema(Schema):
    name = fields.Str(required=False)
    address = fields.Str(required=False)
    description = fields.Str(required=False, allow_none=True)
    status = fields.Str(
        required=False,
        validate=validate.OneOf(["ACTIVE", "INACTIVE"])
    )

class WarehouseResponseSchema(Schema):
    id = fields.Int(required=True)
    household_id = fields.Int(required=True)
    name = fields.Str(required=True)
    address = fields.Str(required=True)
    description = fields.Str(required=False, allow_none=True)
    status = fields.Str(required=True)
    created_at = fields.Raw(required=True)
    updated_at = fields.Raw(required=True)
