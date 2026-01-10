from flask import Flask, jsonify
from src.api.swagger import spec
from src.api.middleware import middleware
from src.infrastructure.databases import init_db
from src.config import Config
from flasgger import Swagger
from src.config import SwaggerConfig
from flask_swagger_ui import get_swaggerui_blueprint
from src.api.routes import register_routes


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    Swagger(app)
    
    # Register all routes via helper function
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
            # Include all prefixes from both HEAD and Main
            if rule.endpoint.startswith(('todo.', 'course.', 'user.', 'auth.',
                                        'owner_invoice.', 'employee_invoice.', 'draft_order.', 'invoice_detail.',
                                        'admin_', 'owner_', 'public_')):
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
            return f"Error loading guide: {str(e)}", 500

    return app

# Run the application

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=9999, debug=True)