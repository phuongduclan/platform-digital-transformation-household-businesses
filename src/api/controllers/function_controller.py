from flask import Blueprint, request, jsonify
from services.function_service import FunctionService
from infrastructure.repositories.function_repository import FunctionRepository
from api.schemas.function import FunctionRequestSchema, FunctionResponseSchema, FunctionUpdateSchema
from infrastructure.databases.mssql import session
from api.decorators.auth_decorators import require_permission

bp = Blueprint('admin_functions', __name__, url_prefix='/api/admin/functions')
function_service = FunctionService(FunctionRepository(session))
request_schema = FunctionRequestSchema()
response_schema = FunctionResponseSchema()
update_schema = FunctionUpdateSchema()

@bp.route('/', methods=['GET'])
@require_permission(function_code="F003", methods=["GET"])
def list_functions():
    """
    List all functions (Admin only)
    ---
    get:
      summary: List all functions
      tags:
        - Admin Functions
      responses:
        200:
          description: List of functions
    """
    functions = function_service.list_functions()
    return jsonify(response_schema.dump(functions, many=True)), 200

@bp.route('/', methods=['POST'])
@require_permission(function_code="F003", methods=["POST"])
def create_function():
    """
    Create function (Admin only)
    ---
    post:
      summary: Create function
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/FunctionRequest'
      tags:
        - Admin Functions
      responses:
        201:
          description: Function created successfully
    """
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    function = function_service.create_function(
        function_code=data['function_code'],
        function_name=data['function_name'],
        url_pattern=data['url_pattern'],
        http_methods=data['http_methods'],
        description=data.get('description'),
        resource_type=data.get('resource_type')
    )
    return jsonify(response_schema.dump(function)), 201

@bp.route('/<int:function_id>', methods=['GET'])
@require_permission(function_code="F003", methods=["GET"])
def get_function(function_id):
    """
    Get function by id (Admin only)
    ---
    get:
      summary: Get function by id
      parameters:
        - name: function_id
          in: path
          required: true
          schema:
            type: integer
      tags:
        - Admin Functions
      responses:
        200:
          description: Function found
        404:
          description: Function not found
    """
    function = function_service.get_function(function_id)
    if not function:
        return jsonify({'message': 'Function not found'}), 404
    return jsonify(response_schema.dump(function)), 200

@bp.route('/<int:function_id>', methods=['PUT'])
@require_permission(function_code="F003", methods=["PUT"])
def update_function(function_id):
    """
    Update function (Admin only)
    ---
    put:
      summary: Update function
      parameters:
        - name: function_id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/FunctionUpdate'
      tags:
        - Admin Functions
      responses:
        200:
          description: Function updated successfully
        404:
          description: Function not found
    """
    data = request.get_json()
    errors = update_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    try:
        function = function_service.update_function(
            function_id=function_id,
            function_code=data.get('function_code'),
            function_name=data.get('function_name'),
            url_pattern=data.get('url_pattern'),
            http_methods=data.get('http_methods'),
            description=data.get('description'),
            resource_type=data.get('resource_type')
        )
        return jsonify(response_schema.dump(function)), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@bp.route('/<int:function_id>', methods=['DELETE'])
@require_permission(function_code="F003", methods=["DELETE"])
def delete_function(function_id):
    """
    Delete function (Admin only)
    ---
    delete:
      summary: Delete function
      parameters:
        - name: function_id
          in: path
          required: true
          schema:
            type: integer
      tags:
        - Admin Functions
      responses:
        204:
          description: Function deleted successfully
        404:
          description: Function not found
    """
    try:
        function_service.delete_function(function_id)
        return '', 204
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
