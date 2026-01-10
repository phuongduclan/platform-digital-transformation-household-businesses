from flask import Flask, jsonify
# from api.routes import register_routes
from api.swagger import spec
from api.controllers.todo_controller import bp as todo_bp
from api.controllers.auth_controller import auth_bp as auth_bp
from api.controllers.invoice_controller import owner_invoice_bp, employee_invoice_bp, draft_order_bp
from api.controllers.invoice_detail_controller import invoice_detail_bp
from api.middleware import middleware
from api.responses import success_response
from infrastructure.databases import init_db
from config import Config
from flasgger import Swagger
from config import SwaggerConfig
from flask_swagger_ui import get_swaggerui_blueprint


def create_app():
    app = Flask(__name__)
    Swagger(app)
    # Đăng ký blueprint trước
    app.register_blueprint(todo_bp)
    app.register_blueprint(auth_bp)
    
    # Invoice blueprints
    app.register_blueprint(owner_invoice_bp)
    app.register_blueprint(employee_invoice_bp)
    app.register_blueprint(draft_order_bp)
    app.register_blueprint(invoice_detail_bp)
    # register_routes(app)
     # Thêm Swagger UI blueprint
    SWAGGER_URL = '/docs'
    API_URL = '/swagger.json'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={'app_name': "Todo API"}
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    try:
        init_db(app)
    except Exception as e:
        print(f"Error initializing database: {e}")

    # Register middleware
    middleware(app)

    # Register routes
    with app.test_request_context():
        for rule in app.url_map.iter_rules():
            # Thêm các endpoint khác nếu cần
            if rule.endpoint.startswith(('todo.', 'course.', 'user.', 'auth.', 'owner_invoice.', 'employee_invoice.', 'draft_order.', 'invoice_detail.')):
                view_func = app.view_functions[rule.endpoint]
                print(f"Adding path: {rule.rule} -> {view_func}")
                spec.path(view=view_func)
            
    @app.route("/swagger.json")
    def swagger_json():
        return jsonify(spec.to_dict())

    @app.route("/test-guide")
    def test_guide():
        import markdown
        
        guide_path = '/Users/tranminhtri/.gemini/antigravity/brain/d08a77f4-b473-4402-a81f-ae3ddb056d60/TEST_GUIDE_VI.md'
        try:
            with open(guide_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            html_content = markdown.markdown(content)
            
            # Simple styling
            styled_html = f"""
            <html>
                <head>
                    <title>Invoice Test Guide</title>
                    <style>
                        body {{ font-family: -apple-system, system-ui, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; color: #333; }}
                        pre {{ background-color: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }}
                        code {{ background-color: #f4f4f4; padding: 2px 5px; border-radius: 3px; font-family: monospace; }}
                        h1, h2, h3 {{ color: #2c3e50; }}
                        a {{ color: #3498db; text-decoration: none; }}
                        a:hover {{ text-decoration: underline; }}
                        .btn {{ display: inline-block; background: #28a745; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin-top: 20px; }}
                        .btn:hover {{ background: #218838; }}
                    </style>
                </head>
                <body>
                    {html_content}
                    <hr>
                    <a href="http://localhost:9999/docs" class="btn" target="_blank">👉 Open Swagger UI to Test</a>
                </body>
            </html>
            """
            return styled_html
        except Exception as e:
            return f"Error loading guide: {{str(e)}}", 500

    return app

# Run the application

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=9999, debug=True)