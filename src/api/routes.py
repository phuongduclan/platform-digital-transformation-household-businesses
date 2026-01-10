# Register routes for the Flask application

from src.api.controllers.todo_controller import bp as todo_bp
from src.api.controllers.auth_controller import auth_bp as auth_bp
from src.api.controllers.invoice_controller import owner_invoice_bp, employee_invoice_bp, draft_order_bp
from src.api.controllers.invoice_detail_controller import invoice_detail_bp

def register_routes(app):
    app.register_blueprint(todo_bp)
    
    # Invoice routes
    app.register_blueprint(owner_invoice_bp)
    app.register_blueprint(employee_invoice_bp)
    app.register_blueprint(draft_order_bp)
    app.register_blueprint(invoice_detail_bp)
    app.register_blueprint(auth_bp)