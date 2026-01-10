from flask import Blueprint, request, jsonify
from services.user_service import UserService
from infrastructure.repositories.user_repository import UserRepository
from api.schemas.user import UserRequestSchema, UserResponseSchema, UserUpdateSchema
from infrastructure.databases.mssql import session
from api.decorators.auth_decorators import require_permission
from api.utils.auth_utils import get_current_household_id

# Admin endpoints
admin_bp = Blueprint('admin_users', __name__, url_prefix='/api/admin/users')
user_service = UserService(UserRepository(session))
request_schema = UserRequestSchema()
response_schema = UserResponseSchema()
update_schema = UserUpdateSchema()

@admin_bp.route('/', methods=['GET'])
@require_permission(function_code="F001", methods=["GET"])
def list_users():
    """
    List all users (Admin only) - CHỈ Admin và Owner, KHÔNG Employee
    ---
    get:
      summary: List all users (Admin and Owner only)
      security:
        - Bearer: []
      tags:
        - Admin Users
      responses:
        200:
          description: List of users (Admin and Owner only)
    """
    # Business rule: Admin chỉ quản lý Admin và Owner (exclude Employee)
    # Business rule được xử lý ở Application Layer (UserService)
    users = user_service.list_users(exclude_employee=True)
    return jsonify(response_schema.dump(users, many=True)), 200

@admin_bp.route('/', methods=['POST'])
@require_permission(function_code="F001", methods=["POST"])
def create_user():
    """
    Create user (Admin only)
    ---
    post:
      summary: Create user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserRequest'
      tags:
        - Admin Users
      responses:
        201:
          description: User created successfully
    """
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    try:
        # Business rule được xử lý ở Application Layer (UserService)
        user = user_service.create_user(
            household_id=data.get('household_id'),
            role_id=data['role_id'],
            user_name=data['user_name'],
            password=data['password'],
            email=data.get('email'),
            description=data.get('description'),
            status=data['status'],
            created_by=data.get('created_by'),
            is_admin_creating=True  # Flag để service check business rule
        )
        return jsonify(response_schema.dump(user)), 201
    except ValueError as e:
        # Business rule violation từ service
        return jsonify({'error': str(e)}), 403

@admin_bp.route('/<int:user_id>', methods=['GET'])
@require_permission(function_code="F001", methods=["GET"])
def get_user(user_id):
    """
    Get user by id (Admin only) - CHỈ Admin và Owner, KHÔNG Employee
    ---
    get:
      summary: Get user by id (Admin and Owner only)
      security:
        - Bearer: []
      parameters:
        - name: user_id
          in: path
          required: true
          schema:
            type: integer
      tags:
        - Admin Users
      responses:
        200:
          description: User found
        403:
          description: Admin cannot access Employee. Use /api/owner/employees/ instead
        404:
          description: User not found
    """
    try:
        # Business rule được xử lý ở Application Layer (UserService)
        user = user_service.get_user(user_id, is_admin_accessing=True)
        if not user:
            return jsonify({'message': 'User not found'}), 404
        return jsonify(response_schema.dump(user)), 200
    except ValueError as e:
        # Business rule violation từ service
        return jsonify({'error': str(e)}), 403

@admin_bp.route('/<int:user_id>', methods=['PUT'])
@require_permission(function_code="F001", methods=["PUT"])
def update_user(user_id):
    """
    Update user (Admin only)
    ---
    put:
      summary: Update user
      parameters:
        - name: user_id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserUpdate'
      tags:
        - Admin Users
      responses:
        200:
          description: User updated successfully
        404:
          description: User not found
    """
    data = request.get_json()
    errors = update_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    try:
        # Business rule được xử lý ở Application Layer (UserService)
        user = user_service.update_user(
            user_id=user_id,
            household_id=data.get('household_id'),
            role_id=data.get('role_id'),
            user_name=data.get('user_name'),
            password=data.get('password'),
            email=data.get('email'),
            description=data.get('description'),
            status=data.get('status'),
            updated_by=data.get('updated_by'),
            is_admin_updating=True  # Flag để service check business rule
        )
        return jsonify(response_schema.dump(user)), 200
    except ValueError as e:
        # Business rule violation hoặc user not found từ service
        if 'not found' in str(e).lower():
            return jsonify({'error': str(e)}), 404
        return jsonify({'error': str(e)}), 403

@admin_bp.route('/<int:user_id>', methods=['DELETE'])
@require_permission(function_code="F001", methods=["DELETE"])
def delete_user(user_id):
    """
    Delete user (Admin only) - CHỈ Admin và Owner, KHÔNG Employee
    ---
    delete:
      summary: Delete user (Admin and Owner only)
      security:
        - Bearer: []
      parameters:
        - name: user_id
          in: path
          required: true
          schema:
            type: integer
      tags:
        - Admin Users
      responses:
        204:
          description: User deleted successfully
        403:
          description: Admin cannot delete Employee. Only Owner can delete Employee via /api/owner/employees/
        404:
          description: User not found
    """
    try:
        # Business rule được xử lý ở Application Layer (UserService)
        user_service.delete_user(user_id, is_admin_deleting=True)
        return '', 204
    except ValueError as e:
        # Business rule violation hoặc user not found từ service
        if 'not found' in str(e).lower():
            return jsonify({'error': str(e)}), 404
        return jsonify({'error': str(e)}), 403

# Owner endpoints
owner_bp = Blueprint('owner_employees', __name__, url_prefix='/api/owner/employees')

@owner_bp.route('/', methods=['GET'])
@require_permission(function_code="F101", methods=["GET"])
def list_employees():
    """
    List employees of household (Owner only)
    ---
    get:
      summary: List employees of household
      security:
        - Bearer: []
      tags:
        - Owner Employees
      responses:
        200:
          description: List of employees
    """
    # Lấy household_id từ JWT token (tự động từ decorator)
    household_id = get_current_household_id()
    if not household_id:
        return jsonify({'error': 'Household ID is required'}), 400
    
    # Filter theo household_id - Data Isolation
    users = user_service.get_users_by_household(household_id)
    return jsonify(response_schema.dump(users, many=True)), 200

@owner_bp.route('/', methods=['POST'])
@require_permission(function_code="F101", methods=["POST"])
def create_employee():
    """
    Create employee (Owner only)
    ---
    post:
      summary: Create employee
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserRequest'
      tags:
        - Owner Employees
      responses:
        201:
          description: Employee created successfully
    """
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    # Lấy household_id từ JWT token (tự động từ decorator)
    household_id = get_current_household_id()
    if not household_id:
        return jsonify({'error': 'Household ID is required'}), 400
    
    user = user_service.create_user(
        household_id=household_id,
        role_id=data['role_id'],
        user_name=data['user_name'],
        password=data['password'],
        email=data.get('email'),
        description=data.get('description'),
        status=data['status'],
        created_by=data.get('created_by')
    )
    return jsonify(response_schema.dump(user)), 201

@owner_bp.route('/<int:employee_id>', methods=['GET'])
@require_permission(function_code="F101", methods=["GET"])
def get_employee(employee_id):
    """
    Get employee by id (Owner only)
    ---
    get:
      summary: Get employee by id
      security:
        - Bearer: []
      parameters:
        - name: employee_id
          in: path
          required: true
          schema:
            type: integer
      tags:
        - Owner Employees
      responses:
        200:
          description: Employee found
        403:
          description: Employee does not belong to your household
        404:
          description: Employee not found
    """
    # Lấy household_id từ JWT token
    household_id = get_current_household_id()
    if not household_id:
        return jsonify({'error': 'Household ID is required'}), 400
    
    # Get employee và check Data Isolation
    user = user_service.get_user(employee_id)
    if not user:
        return jsonify({'message': 'Employee not found'}), 404
    
    # Check employee thuộc household của owner
    if user.household_id != household_id:
        return jsonify({'error': 'Employee does not belong to your household'}), 403
    
    return jsonify(response_schema.dump(user)), 200

@owner_bp.route('/<int:employee_id>', methods=['PUT'])
@require_permission(function_code="F101", methods=["PUT"])
def update_employee(employee_id):
    """
    Update employee (Owner only)
    ---
    put:
      summary: Update employee
      security:
        - Bearer: []
      parameters:
        - name: employee_id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserUpdate'
      tags:
        - Owner Employees
      responses:
        200:
          description: Employee updated successfully
        403:
          description: Employee does not belong to your household
        404:
          description: Employee not found
    """
    # Lấy household_id từ JWT token
    household_id = get_current_household_id()
    if not household_id:
        return jsonify({'error': 'Household ID is required'}), 400
    
    # Check employee thuộc household của owner trước khi update
    existing_user = user_service.get_user(employee_id)
    if not existing_user:
        return jsonify({'error': 'Employee not found'}), 404
    
    if existing_user.household_id != household_id:
        return jsonify({'error': 'Employee does not belong to your household'}), 403
    
    data = request.get_json()
    errors = update_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    try:
        # Đảm bảo household_id không thể thay đổi (force = household_id của owner)
        user = user_service.update_user(
            user_id=employee_id,
            household_id=household_id,  # Force household_id từ JWT
            role_id=data.get('role_id'),
            user_name=data.get('user_name'),
            password=data.get('password'),
            email=data.get('email'),
            description=data.get('description'),
            status=data.get('status'),
            updated_by=data.get('updated_by')
        )
        return jsonify(response_schema.dump(user)), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@owner_bp.route('/<int:employee_id>', methods=['DELETE'])
@require_permission(function_code="F101", methods=["DELETE"])
def delete_employee(employee_id):
    """
    Delete employee (Owner only)
    ---
    delete:
      summary: Delete employee
      security:
        - Bearer: []
      parameters:
        - name: employee_id
          in: path
          required: true
          schema:
            type: integer
      tags:
        - Owner Employees
      responses:
        204:
          description: Employee deleted successfully
        403:
          description: Employee does not belong to your household
        404:
          description: Employee not found
    """
    # Lấy household_id từ JWT token
    household_id = get_current_household_id()
    if not household_id:
        return jsonify({'error': 'Household ID is required'}), 400
    
    # Check employee thuộc household của owner trước khi delete
    existing_user = user_service.get_user(employee_id)
    if not existing_user:
        return jsonify({'error': 'Employee not found'}), 404
    
    if existing_user.household_id != household_id:
        return jsonify({'error': 'Employee does not belong to your household'}), 403
    
    try:
        user_service.delete_user(employee_id)
        return '', 204
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
