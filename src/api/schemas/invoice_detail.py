from marshmallow import Schema, fields, validate
from decimal import Decimal

class InvoiceDetailRequestSchema(Schema):
    product_id = fields.Int(required=True)
    unit_id = fields.Int(required=True)
    quantity = fields.Int(required=True, validate=validate.Range(min=1))
    price = fields.Decimal(required=True, as_string=True)
    vat = fields.Int(required=False, load_default=0, validate=validate.Range(min=0, max=100))
    discount = fields.Int(required=False, load_default=0, validate=validate.Range(min=0, max=100))
    description = fields.Str(required=False, allow_none=True)
    status = fields.Str(
        required=False,
        validate=validate.OneOf(["Draft", "Confirm", "Delete"]),
        load_default="Draft"
    )

class InvoiceDetailUpdateSchema(Schema):
    product_id = fields.Int(required=False, allow_none=True)
    unit_id = fields.Int(required=False, allow_none=True)
    quantity = fields.Int(required=False, validate=validate.Range(min=1), allow_none=True)
    price = fields.Decimal(required=False, as_string=True, allow_none=True)
    vat = fields.Int(required=False, validate=validate.Range(min=0, max=100), allow_none=True)
    discount = fields.Int(required=False, validate=validate.Range(min=0, max=100), allow_none=True)
    description = fields.Str(required=False, allow_none=True)

class InvoiceDetailResponseSchema(Schema):
    id = fields.Int()
    invoice_id = fields.Int()
    product_id = fields.Int()
    unit_id = fields.Int()
    vat = fields.Int()
    discount = fields.Int(allow_none=True)
    price = fields.Decimal(as_string=True)
    description = fields.Str(allow_none=True)
    quantity = fields.Int()
    status = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

class InvoiceDetailListResponseSchema(Schema):
    details = fields.List(fields.Nested(InvoiceDetailResponseSchema))
