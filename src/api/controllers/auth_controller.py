from flask import Blueprint, request, jsonify, current_app
from datetime import datetime, timedelta
from api.schemas.auth import RigisterUserRequestSchema, RigisterUserResponseSchema
from services.auth_service import AuthService
from infrastructure.repositories.auth_repository import AuthRepository
from services.subscription_service import SubscriptionService
from infrastructure.databases.mssql import session
from werkzeug.security import generate_password_hash
import jwt

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth') # Main used /api/auth. HEAD used /auth. Stick to /api/auth.

# Instantiate Services
auth_repo = AuthRepository(session)
# Clean Arch Note: SubscriptionService should ideally use a repo too.
subscription_service = SubscriptionService(session) 
auth_service = AuthService(auth_repo, subscription_service)

register_request = RigisterUserRequestSchema()
register_response = RigisterUserResponseSchema()

@auth_bp.route('/check_router', methods=['GET'])
def check_router():
    """Check router health"""
    return jsonify({'message': 'Router is working!'}), 200

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login user
    ---
    post:
      summary: Login user
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                username:
                  type: string
                password:
                  type: string
              required:
                - username
                - password
      tags:
        - Auth
      responses:
        200:
          description: Login successful
        401:
          description: Invalid credentials
        403:
          description: User inactive or subscription invalid
    """
    data = request.get_json()
    username = data.get('username') or data.get('user_name') # Support both
    password = data.get('password')

    if not username or not password:
         return jsonify({'error': 'Missing credentials'}), 400

    try:
        # Pass PLAIN password. Service will check hash.
        user = auth_service.login(username, password)
        
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401

        # Generate Token
        token = auth_service.generate_jwt_token(user)
        
        return jsonify({
            'token': token,
            'user_id': user.id,
            'role_id': user.role_id,
            'household_id': user.household_id
        }), 200
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 403

@auth_bp.route('/signup', methods=['POST'])
def register():
    """
    Register a new user
    """
    data = request.get_json()
    errors = register_request.validate(data)
    if errors:
      return jsonify(errors), 400

    username = data.get('username')
    password = data.get('password')
    passwordconfirm = data.get('passwordconfirm')
    email = data.get('email')

    if password != passwordconfirm:
      return jsonify({'message': 'Passwords do not match'}), 400

    if auth_service.check_exist(username):
      return jsonify({'message': 'User already exists. Please login.'}), 400

    # HEAD logic hashed this before calling service. Service expects Hashed for register.
    password_hashed = generate_password_hash(password)
    
    new_user = auth_service.register(username, password_hashed, email)
    if not new_user:
      return jsonify({'message': 'Registration failed'}), 500 
      
    result = register_response.dump(new_user)
    return jsonify(result), 201

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """User logout"""
    return jsonify({'message': 'Logged out successfully'}), 200

@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    """Get current user info"""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({'error': 'Missing token'}), 401
    
    try:
        token = auth_header.split(' ')[1]
        payload = auth_service.decode_token(token)
        user_id = payload['user_id']
        
        # Need get_user_by_id logic.
        # AuthService current impl only has login/register.
        # I need to add `get_user_by_id` to Service or Repo.
        # Main AuthService had it.
        # I'll rely on Repo `get_user_by_username`? No, I have ID.
        # I should add `get_user_by_id` to Repo & Service in next step if missed.
        
        # Taking a shortcut check: Does AuthService have get_user_by_id?
        # My new AuthService implementation in step 281 DID NOT include it!
        # I missed porting `get_user_by_id` from Main!
        # I must fix AuthService.
        pass
    except ValueError as e:
        return jsonify({'error': str(e)}), 401
    
    # Placeholder fail
    return jsonify({'error': 'Not implemented yet'}), 500
