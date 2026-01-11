from flask import Blueprint, request, jsonify
from services.auth_service import AuthService
from infrastructure.databases.mssql import session

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
auth_service = AuthService(session)

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    User login
    ---
    post:
      summary: User login
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                user_name:
                  type: string
                password:
                  type: string
              required:
                - user_name
                - password
      tags:
        - Auth
      responses:
        200:
          description: Login successful
          content:
            application/json:
              schema:
                type: object
                properties:
                  token:
                    type: string
                  user_id:
                    type: integer
                  role_id:
                    type: integer
                  household_id:
                    type: integer
        400:
          description: Missing credentials
        401:
          description: Invalid credentials
        403:
          description: User is inactive or subscription not active
    """
    data = request.get_json()
    
    # Validation cơ bản
    if not data or 'user_name' not in data or 'password' not in data:
        return jsonify({'error': 'Missing credentials'}), 400
    
    try:
        # Business logic được xử lý ở Application Layer (AuthService)
        user = auth_service.authenticate_user(data['user_name'], data['password'])
        
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Generate JWT token
        token = auth_service.generate_jwt_token(user)
        
        return jsonify({
            'token': token,
            'user_id': user.id,
            'role_id': user.role_id,
            'household_id': user.household_id
        }), 200
    except ValueError as e:
        # Business rule violation từ service (user inactive)
        return jsonify({'error': str(e)}), 403

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """
    User logout
    ---
    post:
      summary: User logout
      tags:
        - Auth
      responses:
        200:
          description: Logout successful
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
    """
    # JWT stateless nên chỉ return success
    return jsonify({'message': 'Logged out successfully'}), 200

@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    """
    Get current user info
    ---
    get:
      summary: Get current user info
      security:
        - Bearer: []
      tags:
        - Auth
      responses:
        200:
          description: User info
          content:
            application/json:
              schema:
                type: object
                properties:
                  id:
                    type: integer
                  user_name:
                    type: string
                  role_id:
                    type: integer
                  household_id:
                    type: integer
                  email:
                    type: string
        401:
          description: Missing or invalid token
        404:
          description: User not found
    """
    # Lấy token từ header
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Missing token'}), 401
    
    try:
        token = auth_header.split(' ')[1]
        
        # Business logic được xử lý ở Application Layer (AuthService)
        payload = auth_service.decode_token(token)
        user_id = payload['user_id']
        
        user = auth_service.get_user_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify({
            'id': user.id,
            'user_name': user.user_name,
            'role_id': user.role_id,
            'household_id': user.household_id,
            'email': user.email if hasattr(user, 'email') else None
        }), 200
    except ValueError as e:
        # Business rule violation từ service (token expired/invalid)
        return jsonify({'error': str(e)}), 401