from marshmallow import Schema, fields

class DebtRecordResponseSchema(Schema):
    id = fields.Int()
    customer_id = fields.Int()
    invoice_id = fields.Int(allow_none=True)
    payment_id = fields.Int(allow_none=True)
    debit_amount = fields.Decimal(as_string=True, allow_none=True)
    credit_amount = fields.Decimal(as_string=True, allow_none=True)
    balance = fields.Decimal(as_string=True, allow_none=True)
    description = fields.Str(allow_none=True)
    record_at = fields.DateTime()

class DebtRecordListResponseSchema(Schema):
    debt_records = fields.List(fields.Nested(DebtRecordResponseSchema))
