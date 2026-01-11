from api.controllers.todo_controller import bp as todo_bp
from api.controllers.auth_controller import auth_bp
from api.controllers.user_controller import admin_bp as admin_users_bp, owner_bp as owner_employees_bp
from api.controllers.role_controller import bp as admin_roles_bp
from api.controllers.function_controller import bp as admin_functions_bp
from api.controllers.role_function_controller import bp as admin_role_functions_bp
from api.controllers.product_controller import owner_bp as owner_products_bp, employee_bp as employee_products_bp
from api.controllers.category_controller import owner_bp as owner_categories_bp, employee_bp as employee_categories_bp
from api.controllers.unit_controller import owner_bp as owner_units_bp, employee_bp as employee_units_bp
from api.controllers.warehouse_controller import owner_bp as owner_warehouses_bp, employee_bp as employee_warehouses_bp

from api.controllers.household_controller import owner_bp as owner_household_bp
from api.controllers.subscription_plan_controller import admin_bp as admin_subscription_plan_bp, public_bp as public_subscription_plan_bp, owner_bp as owner_subscription_plan_bp
from api.controllers.subscription_controller import admin_bp as admin_subscription_bp, owner_bp as owner_subscription_bp
from api.controllers.registration_controller import bp as public_registration_bp
from api.controllers.invoice_controller import owner_invoice_bp, employee_invoice_bp, draft_order_bp
from api.controllers.invoice_detail_controller import invoice_detail_bp

def register_routes(app):
    # Todo (sample module)
    app.register_blueprint(todo_bp)
    
    # Auth Blueprints
    app.register_blueprint(auth_bp)
    
    # Admin endpoints
    app.register_blueprint(admin_users_bp)
    app.register_blueprint(admin_roles_bp)
    app.register_blueprint(admin_functions_bp)
    app.register_blueprint(admin_role_functions_bp) 

    # Business Blueprints (Products, Categories, etc.)
    app.register_blueprint(owner_products_bp)
    app.register_blueprint(employee_products_bp)
    app.register_blueprint(owner_categories_bp)
    app.register_blueprint(employee_categories_bp)
    app.register_blueprint(owner_units_bp)
    app.register_blueprint(employee_units_bp)
    app.register_blueprint(owner_warehouses_bp)
    app.register_blueprint(employee_warehouses_bp)
    app.register_blueprint(admin_subscription_plan_bp)
    app.register_blueprint(admin_subscription_bp)
    
    # Owner specific
    app.register_blueprint(owner_employees_bp)
    app.register_blueprint(owner_household_bp) 
    app.register_blueprint(owner_subscription_bp)
    app.register_blueprint(owner_subscription_plan_bp)
    
    # Public endpoints
    app.register_blueprint(public_subscription_plan_bp)
    app.register_blueprint(public_registration_bp)

    # Invoice Blueprints (Member 5 Scope)
    app.register_blueprint(owner_invoice_bp)
    app.register_blueprint(employee_invoice_bp)
    app.register_blueprint(draft_order_bp)
    app.register_blueprint(invoice_detail_bp)
