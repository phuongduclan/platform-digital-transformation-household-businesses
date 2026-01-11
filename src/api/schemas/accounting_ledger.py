from marshmallow import Schema, fields, validate

class AccountingLedgerResponseSchema(Schema):
    id = fields.Int()
    invoice_id = fields.Int()
    transaction_date = fields.DateTime()
    description = fields.Str()
    debit_amount = fields.Decimal(as_string=True, allow_none=True)
    credit_amount = fields.Decimal(as_string=True, allow_none=True)
    balance = fields.Decimal(as_string=True, allow_none=True)
    document_number = fields.Str()
    movement_type = fields.Str()
    status = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

class AccountingLedgerListResponseSchema(Schema):
    accounting_ledgers = fields.List(fields.Nested(AccountingLedgerResponseSchema))

class RevenueReportResponseSchema(Schema):
    date = fields.Date(allow_none=True)
    month = fields.Int(allow_none=True)
    year = fields.Int(allow_none=True)
    total_revenue = fields.Decimal(as_string=True)
