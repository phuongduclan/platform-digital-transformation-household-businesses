from marshmallow import Schema, fields, validate

class InvoiceRequestSchema(Schema):
    """Schema for creating/updating invoices"""
    customer_name = fields.Str(required=True, validate=validate.Length(min=1, max=255), metadata={"example": "ABC Corp"})
    invoice_type = fields.Str(required=False, load_default='SALES', validate=validate.OneOf(['SALES', 'PURCHASE']), metadata={"example": "SALES"})
    total_amount = fields.Float(required=False, load_default=0.0, metadata={"example": 150.50})
    discount_total = fields.Float(required=False, load_default=0.0, metadata={"example": 10.0})
    vat_total = fields.Float(required=False, load_default=0.0, metadata={"example": 15.0})
    description = fields.Str(required=False, metadata={"example": "Invoice for January service"})
    status = fields.Str(
        required=False,
        load_default='DRAFT',
        validate=validate.OneOf(['DRAFT', 'CONFIRMED', 'PAID', 'CANCELLED']),
        metadata={"example": "DRAFT"}
    )
    source = fields.Str(
        required=False,
        load_default='MANUAL',
        validate=validate.OneOf(['MANUAL', 'AI']),
        metadata={"example": "MANUAL"}
    )

class InvoiceResponseSchema(Schema):
    """Schema for invoice responses"""
    id = fields.Int(required=True, metadata={"example": 1})
    invoice_number = fields.Str(required=True, metadata={"example": "INV-20260110-0001"})
    customer_name = fields.Str(required=True)
    invoice_type = fields.Str(required=True)
    total_amount = fields.Float(required=True)
    discount_total = fields.Float(required=True)
    vat_total = fields.Float(required=True)
    description = fields.Str(required=False)
    status = fields.Str(required=True)
    source = fields.Str(required=True)
    created_by = fields.Int(required=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)

class InvoiceDetailNestedSchema(Schema):
    """Nested schema for invoice details"""
    id = fields.Int(required=True)
    product_name = fields.Str(required=True)
    quantity = fields.Int(required=True)
    unit_price = fields.Float(required=True)
    subtotal = fields.Float(required=True)

class InvoiceWithDetailsSchema(Schema):
    """Schema for invoice with nested details"""
    id = fields.Int(required=True)
    invoice_number = fields.Str(required=True)
    customer_name = fields.Str(required=True)
    total_amount = fields.Float(required=True)
    status = fields.Str(required=True)
    source = fields.Str(required=True)
    created_by = fields.Int(required=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)
    details = fields.List(fields.Nested(InvoiceDetailNestedSchema))
