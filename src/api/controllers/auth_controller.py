from flask import Blueprint, request, jsonify
from domain.models.iauth_service import IAuthService
from services.auth_service import AuthService
from infrastructure.databases.mssql import session

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')
auth_service: IAuthService = AuthService(session)

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

@auth_bp.route('/me', methods=['PUT'])
def update_current_user():
    """
    Update current user profile (Admin and Owner can update their own info)
    ---
    put:
      summary: Update current user profile
      security:
        - Bearer: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                user_name:
                  type: string
                  description: Optional - Update user_name
                email:
                  type: string
                  description: Optional - Update email
                description:
                  type: string
                  description: Optional - Update description
                password:
                  type: string
                  description: Optional - Update password
      tags:
        - Auth
      responses:
        200:
          description: User profile updated successfully
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
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        # Import user service
        from services.user_service import UserService
        from infrastructure.repositories.user_repository import UserRepository
        from infrastructure.databases.mssql import session
        from infrastructure.databases.session_utils import safe_commit, safe_rollback
        
        user_repository = UserRepository(session)
        user_service = UserService(user_repository)
        
        # Update user - Owner/Admin chỉ update thông tin của chính họ
        # KHÔNG được update status (chỉ Admin mới có thể activate/deactivate qua /api/admin/users/{id})
        update_data = {}
        if 'user_name' in data:
            update_data['user_name'] = data['user_name']
        if 'email' in data:
            update_data['email'] = data.get('email')
        if 'description' in data:
            update_data['description'] = data.get('description')
        if 'password' in data and data['password']:
            update_data['password'] = data['password']
        
        # Get current user for updated_by
        current_user = auth_service.get_user_by_id(user_id)
        if current_user and hasattr(current_user, 'user_name'):
            update_data['updated_by'] = current_user.user_name
        
        if not update_data:
            return jsonify({'error': 'No fields to update'}), 400
        
        # Update user (không dùng is_admin_updating vì đây là self-update)
        # KHÔNG cho phép update status qua API này
        updated_user = user_service.update_user(
            user_id=user_id,
            user_name=update_data.get('user_name'),
            password=update_data.get('password'),
            email=update_data.get('email'),
            description=update_data.get('description'),
            updated_by=update_data.get('updated_by'),
            is_admin_updating=False  # Self-update, không phải admin update
        )
        
        # Commit transaction
        safe_commit(session)
        
        return jsonify({
            'id': updated_user.id,
            'user_name': updated_user.user_name,
            'email': updated_user.email if hasattr(updated_user, 'email') else None,
            'description': updated_user.description if hasattr(updated_user, 'description') else None,
            'message': 'Profile updated successfully'
        }), 200
        
    except ValueError as e:
        safe_rollback(session)
        if 'not found' in str(e).lower():
            return jsonify({'error': str(e)}), 404
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        safe_rollback(session)
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500
