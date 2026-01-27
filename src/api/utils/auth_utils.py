"""
Auth utilities - Lấy thông tin từ JWT token
"""
import jwt
from flask import request, current_app, g, jsonify
from functools import wraps

def get_current_user_id():
    """Lấy user_id từ JWT token (đã decode trong middleware)"""
    return getattr(g, 'user_id', None)

def get_current_role_id():
    """Lấy role_id từ JWT token"""
    return getattr(g, 'role_id', None)

def get_current_household_id():
    """Lấy household_id từ JWT token (None nếu Admin)"""
    return getattr(g, 'household_id', None)

def get_household_id_from_token():
    """Alias for get_current_household_id() - for backward compatibility"""
    return get_current_household_id()

def decode_jwt_token(token):
    """Decode JWT token và trả về payload"""
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError('Token expired')
    except jwt.InvalidTokenError:
        raise ValueError('Invalid token')

def get_token_from_header():
    """Lấy token từ Authorization header"""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    return auth_header.split(' ')[1]

def token_required(f):
    """
    Decorator để check JWT token validity
    Lưu user info vào Flask context (g) và request.user
    
    Usage:
        @bp.route('/endpoint')
        @token_required
        def my_endpoint():
            user_id = g.user_id
            household_id = g.household_id
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Skip OPTIONS requests (CORS preflight)
        if request.method == 'OPTIONS':
            return jsonify({'message': 'OK'}), 200
        
        # 1. Lấy token từ header
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({'error': 'Missing token'}), 401
        
        # Handle both "Bearer token" and raw token
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        else:
            token = auth_header
        
        if not token:
            return jsonify({'error': 'Missing token'}), 401
        
        # 2. Decode token
        try:
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            user_id = payload.get('user_id')
            role_id = payload.get('role_id')
            household_id = payload.get('household_id')
            user_name = payload.get('user_name')
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        
        # 3. Lưu thông tin vào g (Flask context) và request.user
        g.user_id = user_id
        g.role_id = role_id
        g.household_id = household_id
        
        # Set request.user for backward compatibility
        request.user = {
            'user_id': user_id,
            'user_name': user_name,
            'role_id': role_id,
            'household_id': household_id
        }
        
        return f(*args, **kwargs)
    
    return decorated_function
