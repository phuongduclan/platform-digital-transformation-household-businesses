from marshmallow import Schema, fields, validate

class InvoiceDetailRequestSchema(Schema):
    """Schema for creating/updating invoice details"""
    product_name = fields.Str(required=True, validate=validate.Length(min=1, max=255), metadata={"example": "Premium Widget"})
    quantity = fields.Int(required=True, validate=validate.Range(min=1), metadata={"example": 5})
    unit_price = fields.Float(required=True, validate=validate.Range(min=0), metadata={"example": 19.99})
    vat = fields.Float(required=False, load_default=0.0, metadata={"example": 5.0})
    discount = fields.Float(required=False, load_default=0.0, metadata={"example": 2.0})
    description = fields.Str(required=False, metadata={"example": "Special item discount applied"})

class InvoiceDetailResponseSchema(Schema):
    """Schema for invoice detail responses"""
    id = fields.Int(required=True, metadata={"example": 1})
    invoice_id = fields.Int(required=True, metadata={"example": 1})
    product_name = fields.Str(required=True, metadata={"example": "Premium Widget"})
    quantity = fields.Int(required=True, metadata={"example": 5})
    unit_price = fields.Float(required=True, metadata={"example": 19.99})
    vat = fields.Float(required=True)
    discount = fields.Float(required=True)
    description = fields.Str(required=False)
    subtotal = fields.Float(required=True, metadata={"example": 99.95})
