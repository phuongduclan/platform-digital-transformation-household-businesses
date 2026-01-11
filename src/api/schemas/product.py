from marshmallow import Schema, fields, validate


class ProductRequestSchema(Schema):
    category_id = fields.Int(required=True)
    name = fields.Str(required=True)
    image_url = fields.Str(required=False, allow_none=True)
    description = fields.Str(required=False, allow_none=True)
    status = fields.Str(
        required=False,
        validate=validate.OneOf(["ACTIVE", "INACTIVE"]),
        load_default="ACTIVE"
    )

class ProductUpdateSchema(Schema):
    category_id = fields.Int(required=False)
    name = fields.Str(required=False)
    image_url = fields.Str(required=False, allow_none=True)
    description = fields.Str(required=False, allow_none=True)
    status = fields.Str(
        required=False,
        validate=validate.OneOf(["ACTIVE", "INACTIVE"])
    )

class ProductResponseSchema(Schema):
    id = fields.Int()
    household_id = fields.Int()
    category_id = fields.Int()
    name = fields.Str()
    image_url = fields.Str(allow_none=True)
    description = fields.Str(allow_none=True)
    status = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()