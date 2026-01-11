from marshmallow import Schema, fields, validate

class CustomerRequestSchema(Schema):
    tax_code = fields.Str(required=False, allow_none=True)
    name = fields.Str(required=True)
    phone = fields.Str(required=False, allow_none=True)
    address = fields.Str(required=False, allow_none=True)
    description = fields.Str(required=False, allow_none=True)
    status = fields.Str(
        required=False,
        validate=validate.OneOf(["Active", "Inactive"]),
        load_default="Active"
    )

class CustomerUpdateSchema(Schema):
    tax_code = fields.Str(required=False, allow_none=True)
    name = fields.Str(required=False)
    phone = fields.Str(required=False, allow_none=True)
    address = fields.Str(required=False, allow_none=True)
    description = fields.Str(required=False, allow_none=True)
    status = fields.Str(
        required=False,
        validate=validate.OneOf(["Active", "Inactive"])
    )

class CustomerResponseSchema(Schema):
    id = fields.Int()
    household_id = fields.Int()
    tax_code = fields.Str(allow_none=True)
    name = fields.Str()
    phone = fields.Str(allow_none=True)
    address = fields.Str(allow_none=True)
    description = fields.Str(allow_none=True)
    status = fields.Str()
    created_by = fields.Str(allow_none=True)
    updated_by = fields.Str(allow_none=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

class CustomerListResponseSchema(Schema):
    customers = fields.List(fields.Nested(CustomerResponseSchema))
