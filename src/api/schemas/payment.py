from marshmallow import Schema, fields, validate

class PaymentRequestSchema(Schema):
    invoice_id = fields.Int(required=True)
    method_id = fields.Int(required=True)
    amount = fields.Decimal(required=True, as_string=True)
    description = fields.Str(required=False, allow_none=True)

class PaymentUpdateSchema(Schema):
    method_id = fields.Int(required=False)
    amount = fields.Decimal(required=False, as_string=True)
    description = fields.Str(required=False, allow_none=True)

class PaymentResponseSchema(Schema):
    id = fields.Int()
    invoice_id = fields.Int()
    method_id = fields.Int()
    amount = fields.Decimal(as_string=True)
    description = fields.Str(allow_none=True)
    status = fields.Str()
    created_by = fields.Str(allow_none=True)
    updated_by = fields.Str(allow_none=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

class PaymentListResponseSchema(Schema):
    payments = fields.List(fields.Nested(PaymentResponseSchema))
