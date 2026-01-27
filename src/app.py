from flask import Flask, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
from api.swagger import spec
from api.middleware import middleware
from infrastructure.databases import init_db
from config import Config
from flasgger import Swagger
from config import SwaggerConfig
from flask_swagger_ui import get_swaggerui_blueprint
from api.routes import register_routes

# Initialize SocketIO (will be configured in create_app)
socketio = None


def create_app():
    global socketio
    
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize SocketIO
    socketio = SocketIO(
        app,
        cors_allowed_origins="*",  # Allow all origins for development
        async_mode='threading'
    )
    
    # Enable CORS for all routes (cho phép FE gọi API từ localhost:3000)
    # Flask-CORS will automatically handle OPTIONS preflight requests
    CORS(app, 
         resources={r"/*": {
             "origins": "*",
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
             "allow_headers": ["Content-Type", "Authorization"],
             "expose_headers": ["Content-Type"]
         }})
    
    Swagger(app)
    
    # Register all routes
    register_routes(app)

     # Thêm Swagger UI blueprint
    SWAGGER_URL = '/docs'
    API_URL = '/swagger.json'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={'app_name': "BizFlow API"}
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    try:
        init_db(app)
    except Exception as e:
        print(f"Error initializing database: {e}")

    # Register middleware
    middleware(app)

    # Register routes for Swagger
    with app.test_request_context():
        for rule in app.url_map.iter_rules():
            if rule.endpoint.startswith(('todo.', 'auth.', 'admin_', 'owner_', 'employee_', 'public')):
                view_func = app.view_functions[rule.endpoint]
                spec.path(view=view_func)

    @app.route("/swagger.json")
    def swagger_json():
        return jsonify(spec.to_dict())
    
    # SocketIO event handlers
    @socketio.on('connect')
    def handle_connect():
        print(f'Client connected')
    
    @socketio.on('disconnect')
    def handle_disconnect():
        print(f'Client disconnected')
    
    @socketio.on('join_household')
    def handle_join_household(data):
        """Client joins household room to receive notifications"""
        from services.notification_service import NotificationService
        household_id = data.get('household_id')
        if household_id:
            notification_service = NotificationService(socketio)
            notification_service.join_household_room(household_id)
            print(f'Client joined household_{household_id}')

    return app


def get_socketio():
    """Get SocketIO instance"""
    return socketio


if __name__ == '__main__':
    app = create_app()
    # Use socketio.run instead of app.run for WebSocket support
    socketio.run(app, host='0.0.0.0', port=6868, debug=True)