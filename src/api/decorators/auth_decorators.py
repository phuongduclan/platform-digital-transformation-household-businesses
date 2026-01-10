"""
Auth Decorators - Check permission, role, subscription
"""
from functools import wraps
from flask import jsonify, request, g, current_app
import jwt
from services.permission_service import PermissionService
from services.subscription_service import SubscriptionService
from infrastructure.databases.mssql import session
from infrastructure.models import User

permission_service = PermissionService(session)
subscription_service = SubscriptionService(session)

def require_permission(function_code, methods=None):
    """
    Decorator để check permission
    
    Args:
        function_code: Code của function (F001, F101, etc.)
        methods: List HTTP methods được phép (['GET', 'POST'], None = tất cả)
    
    Usage:
        @bp.route('/products', methods=['GET'])
        @require_permission(function_code="F104", methods=["GET"])
        def list_products():
            pass
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # 1. Lấy token từ header
            auth_header = request.headers.get('Authorization')
            
            if not auth_header:
                return jsonify({'error': 'Missing token', 'debug': 'No Authorization header found'}), 401
            
            # Swagger UI có thể gửi token không có "Bearer " prefix
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
            else:
                # Nếu không có "Bearer ", thử dùng trực tiếp
                token = auth_header
                auth_header = f'Bearer {token}'
            
            if not token:
                return jsonify({'error': 'Missing token', 'debug': 'Token is empty'}), 401
            
            try:
                payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
                user_id = payload.get('user_id')
                role_id = payload.get('role_id')
                household_id = payload.get('household_id')
            except jwt.ExpiredSignatureError:
                return jsonify({'error': 'Token expired'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'error': 'Invalid token'}), 401
            
            # 2. Check user có tồn tại và active không
            user = session.query(User).filter_by(id=user_id).first()
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            if hasattr(user, 'status') and user.status.upper() != 'ACTIVE':
                return jsonify({'error': 'User is inactive'}), 403
            
            # 3. Check role có function code không
            http_method = request.method
            if methods and http_method not in methods:
                return jsonify({'error': f'Method {http_method} not allowed'}), 405
            
            has_permission = permission_service.check_role_has_function(
                role_id=role_id,
                function_code=function_code,
                http_method=http_method
            )
            
            if not has_permission:
                return jsonify({
                    'error': f'Permission denied. Role {role_id} does not have function {function_code} with method {http_method}'
                }), 403
            
            # 4. Check subscription (nếu Owner/Employee)
            if household_id:  # Không phải Admin
                if not subscription_service.check_household_subscription_active(household_id):
                    return jsonify({'error': 'Household subscription is not active'}), 403
            
            # 5. Lưu thông tin vào g (Flask context) để dùng trong controller
            g.user_id = user_id
            g.role_id = role_id
            g.household_id = household_id
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator
