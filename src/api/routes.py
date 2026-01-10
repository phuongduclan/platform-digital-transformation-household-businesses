# Register routes for the Flask application

from src.api.controllers.todo_controller import bp as todo_bp
from src.api.controllers.auth_controller import auth_bp
from src.api.controllers.invoice_controller import owner_invoice_bp, employee_invoice_bp, draft_order_bp
from src.api.controllers.invoice_detail_controller import invoice_detail_bp

from src.api.controllers.user_controller import admin_bp as admin_users_bp, owner_bp as owner_employees_bp
from src.api.controllers.role_controller import bp as admin_roles_bp
from src.api.controllers.function_controller import bp as admin_functions_bp
from src.api.controllers.role_function_controller import bp as admin_role_functions_bp

from src.api.controllers.household_controller import owner_bp as owner_household_bp
from src.api.controllers.subscription_plan_controller import admin_bp as admin_subscription_plan_bp, public_bp as public_subscription_plan_bp, owner_bp as owner_subscription_plan_bp
from src.api.controllers.subscription_controller import admin_bp as admin_subscription_bp, owner_bp as owner_subscription_bp
from src.api.controllers.registration_controller import bp as public_registration_bp

def register_routes(app):
    # Todo (sample module)
    app.register_blueprint(todo_bp)
    
    # Auth
    app.register_blueprint(auth_bp)
    
    # Invoice Blueprints (from main branch)
    app.register_blueprint(owner_invoice_bp)
    app.register_blueprint(employee_invoice_bp)
    app.register_blueprint(draft_order_bp)
    app.register_blueprint(invoice_detail_bp)
    
    # Admin/User Blueprints
    app.register_blueprint(admin_users_bp)
    app.register_blueprint(admin_roles_bp)
    app.register_blueprint(admin_functions_bp)
    app.register_blueprint(admin_role_functions_bp)
    
    # Admin endpoints
    app.register_blueprint(admin_subscription_plan_bp)
    app.register_blueprint(admin_subscription_bp)
    
    # Owner endpoints
    app.register_blueprint(owner_employees_bp)
    app.register_blueprint(owner_household_bp)  # Owner quản lý household của mình (F102)
    app.register_blueprint(owner_subscription_bp)  # Owner tự quản lý subscription của mình (upgrade plan)
    app.register_blueprint(owner_subscription_plan_bp)  # Owner xem subscription plans để upgrade (F102)
    
    # Public endpoints (không cần auth)
    app.register_blueprint(public_subscription_plan_bp)  # GET /api/public/subscription-plans
    app.register_blueprint(public_registration_bp)  # POST /api/public/register
