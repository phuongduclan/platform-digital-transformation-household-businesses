# src/api/schemas/subscription.py
from marshmallow import Schema, fields

class SubscriptionRequestSchema(Schema):
    plan_id = fields.Int(required=True)
    household_id = fields.Int(required=True)
    start_date = fields.DateTime(required=False, load_default=None)
    end_date = fields.DateTime(required=False, load_default=None)
    is_active = fields.Bool(required=False, load_default=True)

class SubscriptionResponseSchema(Schema):
    id = fields.Int(required=True)
    plan_id = fields.Int(required=True)
    household_id = fields.Int(required=True)
    start_date = fields.DateTime(required=True)
    end_date = fields.DateTime(required=True)
    is_active = fields.Bool(required=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)
