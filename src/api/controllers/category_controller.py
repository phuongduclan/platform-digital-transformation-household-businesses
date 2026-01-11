from flask import Blueprint, request, g, jsonify
from services.category_service import CategoryService
from infrastructure.repositories.category_repository import CategoryRepository
from api.decorators.auth_decorators import require_permission

# =====================================================
# BLUEPRINTS
# =====================================================

owner_bp = Blueprint(
    "owner_categories",
    __name__,
    url_prefix="/api/owner/categories"
)

employee_bp = Blueprint(
    "employee_categories",
    __name__,
    url_prefix="/api/employee/categories"
)

category_service = CategoryService(CategoryRepository())


# =====================================================
# HELPER
# =====================================================

def category_to_dict(c):
    return {
        "id": c.id,
        "household_id": c.household_id,
        "name": c.name,
        "description": c.description,
        "status": c.status,
        "created_at": c.created_at.isoformat() if c.created_at else None,
        "updated_at": c.updated_at.isoformat() if c.updated_at else None
    }

def get_json_or_415():
    if not request.is_json:
        return None, (jsonify({
            "error": "Content-Type must be application/json"
        }), 415)

    return request.get_json(), None
# =====================================================
# OWNER – F103
# =====================================================

@owner_bp.route("", methods=["GET"])
@require_permission("F103", ["GET"])
def owner_list_categories():
    """
    List categories (Owner)
    ---
    get:
      summary: List categories
      tags: [Owner Categories]
      security: [{Bearer: []}]
      responses:
        200:
          description: List of categories
    """
    categories = category_service.list_categories(g.household_id)
    return jsonify([category_to_dict(c) for c in categories]), 200

@owner_bp.route("", methods=["POST"])
@require_permission("F103", ["POST"])
def owner_create_category():
    """
    Create category (Owner)
    ---
    post:
      summary: Create category
      tags: [Owner Categories]
      security:
        - Bearer: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - name
              properties:
                name:
                  type: string
                description:
                  type: string
                status:
                  type: string
                  enum: [ACTIVE, INACTIVE]
      responses:
        201:
          description: Category created
    """
    data = request.get_json()   

    category = category_service.create_category(
        household_id=g.household_id,
        name=data["name"],
        description=data.get("description"),
        status=data.get("status", "ACTIVE")
    )

    return jsonify(category_to_dict(category)), 201



@owner_bp.route("/<int:category_id>", methods=["GET"])
@require_permission("F103", ["GET"])
def owner_get_category(category_id):
    """
    Get category by id (Owner)
    ---
    get:
      summary: Get category
      tags: [Owner Categories]
      security: [{Bearer: []}]
      parameters:
        - name: category_id
          in: path
          required: true
          type: integer
      responses:
        200:
          description: Category detail
        404:
          description: Not found
    """
    category = category_service.get_category(category_id, g.household_id)
    if not category:
        return jsonify({"error": "Category not found"}), 404

    return jsonify(category_to_dict(category)), 200


@owner_bp.route("/<int:category_id>", methods=["PUT"])
@require_permission("F103", ["PUT"])
def owner_update_category(category_id):
    """
    Update category (Owner)
    ---
    put:
      summary: Update category
      tags: [Owner Categories]
      security:
        - Bearer: []
      parameters:
        - name: category_id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                name:
                  type: string
                description:
                  type: string
                status:
                  type: string
                  enum: [ACTIVE, INACTIVE]
      responses:
        200:
          description: Updated
        404:
          description: Not found
    """
    data = request.get_json()

    category = category_service.update_category(
        category_id=category_id,
        household_id=g.household_id,
        name=data.get("name"),
        description=data.get("description"),
        status=data.get("status")
    )

    if not category:
        return jsonify({"error": "Category not found"}), 404

    return jsonify(category_to_dict(category)), 200


@owner_bp.route("/<int:category_id>", methods=["DELETE"])
@require_permission("F103", ["DELETE"])
def owner_delete_category(category_id):
    """
    Delete category (Owner)
    ---
    delete:
      summary: Delete category
      tags: [Owner Categories]
      security: [{Bearer: []}]
      parameters:
        - name: category_id
          in: path
          required: true
          type: integer
      responses:
        204:
          description: Deleted
    """
    category_service.delete_category(category_id, g.household_id)
    return "", 204


# =====================================================
# EMPLOYEE – F202 (READ ONLY)
# =====================================================

@employee_bp.route("", methods=["GET"])
@require_permission("F202", ["GET"])
def employee_list_categories():
    """
    List categories (Employee – read only)
    ---
    get:
      summary: List categories
      tags: [Employee Categories]
      security: [{Bearer: []}]
      responses:
        200:
          description: List of categories
    """
    categories = category_service.list_categories(g.household_id)
    return jsonify([category_to_dict(c) for c in categories]), 200
