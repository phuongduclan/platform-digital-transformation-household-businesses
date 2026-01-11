from marshmallow import Schema, fields, validate

class CategoryRequestSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(required=False, allow_none=True)
    status = fields.Str(
        required=False,
        validate=validate.OneOf(["ACTIVE", "INACTIVE"]),
        load_default="ACTIVE"
    )

class CategoryUpdateSchema(Schema):
    name = fields.Str(required=False)
    description = fields.Str(required=False, allow_none=True)
    status = fields.Str(
        required=False,
        validate=validate.OneOf(["ACTIVE", "INACTIVE"])
    )
    
class CategoryResponseSchema(Schema):
    id = fields.Int(required=True)
    household_id = fields.Int(required=True)
    name = fields.Str(required=True)
    description = fields.Str(required=False, allow_none=True)
    status = fields.Str(required=True)
    created_at = fields.Raw(required=True)
    updated_at = fields.Raw(required=True)
