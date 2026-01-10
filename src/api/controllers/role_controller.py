from flask import Blueprint, request, jsonify
from services.role_service import RoleService
from infrastructure.repositories.role_repository import RoleRepository
from api.schemas.role import RoleRequestSchema, RoleResponseSchema, RoleUpdateSchema
from infrastructure.databases.mssql import session
from api.decorators.auth_decorators import require_permission

bp = Blueprint('admin_roles', __name__, url_prefix='/api/admin/roles')
role_service = RoleService(RoleRepository(session))
request_schema = RoleRequestSchema()
response_schema = RoleResponseSchema()
update_schema = RoleUpdateSchema()

@bp.route('/', methods=['GET'])
@require_permission(function_code="F002", methods=["GET"])
def list_roles():
    """
    List all roles (Admin only)
    ---
    get:
      summary: List all roles
      security:
        - Bearer: []
      tags:
        - Admin Roles
      responses:
        200:
          description: List of roles
    """
    roles = role_service.list_roles()
    return jsonify(response_schema.dump(roles, many=True)), 200

@bp.route('/', methods=['POST'])
@require_permission(function_code="F002", methods=["POST"])
def create_role():
    """
    Create role (Admin only)
    ---
    post:
      summary: Create role
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/RoleRequest'
      tags:
        - Admin Roles
      responses:
        201:
          description: Role created successfully
    """
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    role = role_service.create_role(
        role_name=data['role_name'],
        description=data.get('description')
    )
    return jsonify(response_schema.dump(role)), 201

@bp.route('/<int:role_id>', methods=['GET'])
@require_permission(function_code="F002", methods=["GET"])
def get_role(role_id):
    """
    Get role by id (Admin only)
    ---
    get:
      summary: Get role by id
      parameters:
        - name: role_id
          in: path
          required: true
          schema:
            type: integer
      tags:
        - Admin Roles
      responses:
        200:
          description: Role found
        404:
          description: Role not found
    """
    role = role_service.get_role(role_id)
    if not role:
        return jsonify({'message': 'Role not found'}), 404
    return jsonify(response_schema.dump(role)), 200

@bp.route('/<int:role_id>', methods=['PUT'])
@require_permission(function_code="F002", methods=["PUT"])
def update_role(role_id):
    """
    Update role (Admin only)
    ---
    put:
      summary: Update role
      parameters:
        - name: role_id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/RoleUpdate'
      tags:
        - Admin Roles
      responses:
        200:
          description: Role updated successfully
        404:
          description: Role not found
    """
    data = request.get_json()
    errors = update_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    try:
        role = role_service.update_role(
            role_id=role_id,
            role_name=data.get('role_name'),
            description=data.get('description')
        )
        return jsonify(response_schema.dump(role)), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@bp.route('/<int:role_id>', methods=['DELETE'])
@require_permission(function_code="F002", methods=["DELETE"])
def delete_role(role_id):
    """
    Delete role (Admin only)
    ---
    delete:
      summary: Delete role
      parameters:
        - name: role_id
          in: path
          required: true
          schema:
            type: integer
      tags:
        - Admin Roles
      responses:
        204:
          description: Role deleted successfully
        404:
          description: Role not found
    """
    try:
        role_service.delete_role(role_id)
        return '', 204
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
