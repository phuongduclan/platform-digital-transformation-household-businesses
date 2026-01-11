from marshmallow import Schema, fields, validate

class PaymentMethodRequestSchema(Schema):
    name = fields.Str(required=True)
    status = fields.Str(
        required=False,
        validate=validate.OneOf(["Active", "Inactive"]),
        load_default="Active"
    )

class PaymentMethodResponseSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    status = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

class PaymentMethodListResponseSchema(Schema):
    payment_methods = fields.List(fields.Nested(PaymentMethodResponseSchema))
