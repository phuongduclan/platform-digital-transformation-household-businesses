# src/api/schemas/subscription_plan.py

from marshmallow import Schema, fields, EXCLUDE

class SubscriptionPlanRequestSchema(Schema):
    class Meta:
        unknown = EXCLUDE  # bỏ qua các field không định nghĩa, tránh lỗi validate

    name = fields.Str(required=True)
    user_id = fields.Int(required=True)  # bắt buộc, lấy từ user login
    billing_cycle = fields.Str(required=False, allow_none=True)
    price = fields.Float(required=True)  # kiểu số
    description = fields.Str(required=False, allow_none=True)
    status = fields.Str(required=False,  load_default="active")  # mặc định active nếu không gửi

class SubscriptionPlanResponseSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)
    user_id = fields.Int(required=True)
    billing_cycle = fields.Str(required=False, allow_none=True)
    price = fields.Float(required=True)
    description = fields.Str(required=False, allow_none=True)
    status = fields.Str(required=True)
    created_by = fields.Str(required=False, allow_none=True)
    updated_by = fields.Str(required=False, allow_none=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)
