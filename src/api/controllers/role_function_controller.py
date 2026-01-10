from flask import Blueprint, request, jsonify
from services.role_function_service import RoleFunctionService
from infrastructure.repositories.role_function_repository import RoleFunctionRepository
from api.schemas.role_function import RoleFunctionRequestSchema, RoleFunctionResponseSchema
from infrastructure.databases.mssql import session
from api.decorators.auth_decorators import require_permission

bp = Blueprint('admin_role_functions', __name__, url_prefix='/api/admin/roles')
role_function_service = RoleFunctionService(RoleFunctionRepository(session))
request_schema = RoleFunctionRequestSchema()
response_schema = RoleFunctionResponseSchema()

@bp.route('/<int:role_id>/functions', methods=['GET'])
@require_permission(function_code="F002", methods=["GET"])
def get_role_functions(role_id):
    """
    Get functions of role (Admin only)
    ---
    get:
      summary: Get functions of role
      parameters:
        - name: role_id
          in: path
          required: true
          schema:
            type: integer
      tags:
        - Admin Role Functions
      responses:
        200:
          description: List of functions
    """
    role_functions = role_function_service.get_functions_by_role(role_id)
    return jsonify(response_schema.dump(role_functions, many=True)), 200

@bp.route('/<int:role_id>/functions', methods=['POST'])
@require_permission(function_code="F002", methods=["POST"])
def assign_function_to_role(role_id):
    """
    Assign function to role (Admin only)
    ---
    post:
      summary: Assign function to role
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
              $ref: '#/components/schemas/RoleFunctionRequest'
      tags:
        - Admin Role Functions
      responses:
        201:
          description: Function assigned successfully
    """
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    role_function = role_function_service.assign_function_to_role(
        role_id=role_id,
        function_id=data['function_id']
    )
    return jsonify(response_schema.dump(role_function)), 201

@bp.route('/<int:role_id>/functions/<int:function_id>', methods=['DELETE'])
@require_permission(function_code="F002", methods=["DELETE"])
def remove_function_from_role(role_id, function_id):
    """
    Remove function from role (Admin only)
    ---
    delete:
      summary: Remove function from role
      parameters:
        - name: role_id
          in: path
          required: true
          schema:
            type: integer
        - name: function_id
          in: path
          required: true
          schema:
            type: integer
      tags:
        - Admin Role Functions
      responses:
        204:
          description: Function removed successfully
        404:
          description: RoleFunction not found
    """
    try:
        role_function_service.remove_function_from_role(role_id, function_id)
        return '', 204
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
