from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from api.schemas.todo import TodoRequestSchema, TodoResponseSchema
from api.schemas.user import UserRequestSchema, UserResponseSchema, UserUpdateSchema
from api.schemas.role import RoleRequestSchema, RoleResponseSchema, RoleUpdateSchema
from api.schemas.function import FunctionRequestSchema, FunctionResponseSchema, FunctionUpdateSchema
from api.schemas.role_function import RoleFunctionRequestSchema, RoleFunctionResponseSchema

spec = APISpec(
    title='Member 5: Invoice Module',
    version="1.0.0",
    openapi_version='2.0',
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)

# Thêm Bearer token security scheme
spec.components.security_scheme(
    "Bearer",
    {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
        "description": "Nhập token JWT từ /api/auth/login. Chỉ cần dán token, không cần chữ 'Bearer'"
    }
)

# Thêm security mặc định cho tất cả endpoints (trừ login)
spec.options = {"security": [{"Bearer": []}]}

# Common schemas
spec.components.schema("TodoRequest", schema=TodoRequestSchema)
spec.components.schema("TodoResponse", schema=TodoResponseSchema)

# User / Admin schemas
spec.components.schema("UserRequest", schema=UserRequestSchema)
spec.components.schema("UserResponse", schema=UserResponseSchema)
spec.components.schema("UserUpdate", schema=UserUpdateSchema)
spec.components.schema("RoleRequest", schema=RoleRequestSchema)
spec.components.schema("RoleResponse", schema=RoleResponseSchema)
spec.components.schema("RoleUpdate", schema=RoleUpdateSchema)
spec.components.schema("FunctionRequest", schema=FunctionRequestSchema)
spec.components.schema("FunctionResponse", schema=FunctionResponseSchema)
spec.components.schema("FunctionUpdate", schema=FunctionUpdateSchema)
spec.components.schema("RoleFunctionRequest", schema=RoleFunctionRequestSchema)
spec.components.schema("RoleFunctionResponse", schema=RoleFunctionResponseSchema)

# Auth schemas (Not explicitly defined in this branch, using User schemas or inline)
# Removed invalid imports

# Invoice schemas (Member 5)
from api.schemas.invoice import InvoiceRequestSchema, InvoiceResponseSchema, InvoiceWithDetailsSchema
from api.schemas.invoice_detail import InvoiceDetailRequestSchema, InvoiceDetailResponseSchema
spec.components.schema("InvoiceRequest", schema=InvoiceRequestSchema)
spec.components.schema("InvoiceResponse", schema=InvoiceResponseSchema)
spec.components.schema("InvoiceWithDetails", schema=InvoiceWithDetailsSchema)
spec.components.schema("InvoiceDetailRequest", schema=InvoiceDetailRequestSchema)
spec.components.schema("InvoiceDetailResponse", schema=InvoiceDetailResponseSchema)
