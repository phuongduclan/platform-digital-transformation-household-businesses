"""
Auth utilities - Lấy thông tin từ JWT token
"""
import jwt
from flask import request, current_app, g
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
