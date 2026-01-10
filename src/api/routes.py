# Register routes for the Flask application

from src.api.controllers.todo_controller import bp as todo_bp
from src.api.controllers.auth_controller import auth_bp
from src.api.controllers.invoice_controller import owner_invoice_bp, employee_invoice_bp, draft_order_bp
from src.api.controllers.invoice_detail_controller import invoice_detail_bp

# From Main
from src.api.controllers.user_controller import admin_bp as admin_users_bp, owner_bp as owner_employees_bp
from src.api.controllers.role_controller import bp as admin_roles_bp
from src.api.controllers.function_controller import bp as admin_functions_bp
from src.api.controllers.role_function_controller import bp as admin_role_functions_bp

def register_routes(app):
    app.register_blueprint(todo_bp)
    app.register_blueprint(auth_bp)
    
    # Invoice Blueprints (HEAD)
    app.register_blueprint(owner_invoice_bp)
    app.register_blueprint(employee_invoice_bp)
    app.register_blueprint(draft_order_bp)
    app.register_blueprint(invoice_detail_bp)
    
    # Admin/User Blueprints (Main)
    app.register_blueprint(admin_users_bp)
    app.register_blueprint(owner_employees_bp)
    app.register_blueprint(admin_roles_bp)
    app.register_blueprint(admin_functions_bp)
    app.register_blueprint(admin_role_functions_bp)
