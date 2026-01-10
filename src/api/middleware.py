# Middleware functions for processing requests and responses

from flask import request, jsonify, g, current_app
import jwt

def log_request_info(app):
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())

def handle_options_request():
    return jsonify({'message': 'CORS preflight response'}), 200

def error_handling_middleware(error):
    response = jsonify({'error': str(error)})
    response.status_code = 500
    return response

def add_custom_headers(response):
    response.headers['X-Custom-Header'] = 'Value'
    return response

def decode_jwt_middleware():
    """Decode JWT token và lưu vào Flask context (g)"""
    # Skip cho các endpoint public (login, swagger, docs)
    public_paths = ['/api/auth/login', '/swagger.json', '/docs', '/apidocs']
    if any(request.path.startswith(path) for path in public_paths):
        return
    
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        try:
            token = auth_header.split(' ')[1]
            payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            g.user_id = payload.get('user_id')
            g.role_id = payload.get('role_id')
            g.household_id = payload.get('household_id')
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            # Lỗi sẽ được xử lý bởi decorator
            pass

def middleware(app):
    @app.before_request
    def before_request():
        log_request_info(app)
        decode_jwt_middleware()  # Decode JWT và lưu vào g

    @app.after_request
    def after_request(response):
        return add_custom_headers(response)

    @app.errorhandler(Exception)
    def handle_exception(error):
        return error_handling_middleware(error)

    @app.route('/options', methods=['OPTIONS'])
    def options_route():
        return handle_options_request()