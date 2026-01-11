from marshmallow import Schema, fields, validate

class InvoiceRequestSchema(Schema):
    seller_id = fields.Int(required=False, allow_none=True)
    customer_id = fields.Int(required=False, allow_none=True)
    invoice_type = fields.Str(
        required=False,
        validate=validate.OneOf(["PAID", "UNPAID"]),
        load_default="PAID"
    )
    description = fields.Str(required=False, allow_none=True)
    status = fields.Str(
        required=False,
        validate=validate.OneOf(["Draft", "Confirm", "Delete"]),
        load_default="Draft"
    )

class InvoiceWithDetailsRequestSchema(Schema):
    seller_id = fields.Int(required=False, allow_none=True)
    customer_id = fields.Int(required=False, allow_none=True)
    invoice_type = fields.Str(
        required=False,
        validate=validate.OneOf(["PAID", "UNPAID"]),
        load_default="PAID"
    )
    description = fields.Str(required=False, allow_none=True)
    status = fields.Str(
        required=False,
        validate=validate.OneOf(["Draft", "Confirm", "Delete"]),
        load_default="Draft"
    )
    details = fields.List(fields.Dict(), required=True)

class InvoiceUpdateSchema(Schema):
    seller_id = fields.Int(required=False, allow_none=True)
    customer_id = fields.Int(required=False, allow_none=True)
    invoice_type = fields.Str(
        required=False,
        validate=validate.OneOf(["PAID", "UNPAID"])
    )
    description = fields.Str(required=False, allow_none=True)

class InvoiceResponseSchema(Schema):
    id = fields.Int()
    household_id = fields.Int()
    seller_id = fields.Int(allow_none=True)
    customer_id = fields.Int(allow_none=True)
    invoice_type = fields.Str()
    discount_total = fields.Decimal(as_string=True)
    vat_total = fields.Decimal(as_string=True)
    total_amount = fields.Decimal(as_string=True)
    description = fields.Str(allow_none=True)
    status = fields.Str()
    created_by = fields.Str(allow_none=True)
    updated_by = fields.Str(allow_none=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

class InvoiceListResponseSchema(Schema):
    invoices = fields.List(fields.Nested(InvoiceResponseSchema))
