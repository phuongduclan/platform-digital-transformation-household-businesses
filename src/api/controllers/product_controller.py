from flask import Blueprint, request, g, jsonify
from services.product_service import ProductService
from infrastructure.repositories.product_repository import ProductRepository
from api.decorators.auth_decorators import require_permission

# =====================================================
# BLUEPRINTS
# =====================================================

owner_bp = Blueprint(
    "owner_products",
    __name__,
    url_prefix="/api/owner/products"
)

employee_bp = Blueprint(
    "employee_products",
    __name__,
    url_prefix="/api/employee/products"
)

product_service = ProductService(ProductRepository())


# =====================================================
# HELPER
# =====================================================

def product_to_dict(p):
    return {
        "id": p.id,
        "household_id": p.household_id,
        "category_id": p.category_id,
        "name": p.name,
        "image_url": p.image_url,
        "description": p.description,
        "status": p.status,
        "created_at": p.created_at.isoformat() if p.created_at else None,
        "updated_at": p.updated_at.isoformat() if p.updated_at else None,
    }


# =====================================================
# OWNER – F104
# =====================================================

@owner_bp.route("", methods=["GET"])
@require_permission("F104", ["GET"])
def owner_list_products():
    """
    List products (Owner)
    ---
    get:
      summary: List products
      tags: [Owner Products]
      security: [{Bearer: []}]
      responses:
        200:
          description: List of products
    """
    products = product_service.list_products(g.household_id)
    return jsonify([product_to_dict(p) for p in products]), 200


@owner_bp.route("", methods=["POST"])
@require_permission("F104", ["POST"])
def owner_create_product():
    """
    Create product (Owner)
    ---
    post:
      summary: Create product
      tags: [Owner Products]
      security: [{Bearer: []}]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - category_id
                - name
              properties:
                category_id:
                  type: integer
                name:
                  type: string
                image_url:
                  type: string
                description:
                  type: string
                status:
                  type: string
                  enum: [ACTIVE, INACTIVE]
      responses:
        201:
          description: Product created
    """
    data = request.get_json()

    product = product_service.create_product(
        household_id=g.household_id,
        category_id=data["category_id"],
        name=data["name"],
        image_url=data.get("image_url"),
        description=data.get("description"),
        status=data.get("status", "ACTIVE")
    )

    return jsonify(product_to_dict(product)), 201


@owner_bp.route("/<int:product_id>", methods=["GET"])
@require_permission("F104", ["GET"])
def owner_get_product(product_id):
    """
    Get product by id (Owner)
    ---
    get:
      summary: Get product
      tags: [Owner Products]
      security: [{Bearer: []}]
      parameters:
        - name: product_id
          in: path
          required: true
          type: integer
      responses:
        200:
          description: Product detail
        404:
          description: Not found
    """
    product = product_service.get_product(product_id, g.household_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    return jsonify(product_to_dict(product)), 200


@owner_bp.route("/<int:product_id>", methods=["PUT"])
@require_permission("F104", ["PUT"])
def owner_update_product(product_id):
    """
    Update product (Owner)
    ---
    put:
      summary: Update product
      tags: [Owner Products]
      security:
        - Bearer: []
      parameters:
        - name: product_id
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
                category_id:
                  type: integer
                name:
                  type: string
                image_url:
                  type: string
                description:
                  type: string
                status:
                  type: string
                  enum: [ACTIVE, INACTIVE]
      responses:
        200:
          description: Product updated
        404:
          description: Not found
    """
    data = request.get_json()

    product = product_service.update_product(
        product_id=product_id,
        household_id=g.household_id,
        category_id=data.get("category_id"),
        name=data.get("name"),
        image_url=data.get("image_url"),
        description=data.get("description"),
        status=data.get("status")
    )

    return jsonify(product_to_dict(product)), 200


@owner_bp.route("/<int:product_id>", methods=["DELETE"])
@require_permission("F104", ["DELETE"])
def owner_delete_product(product_id):
    """
    Delete product (Owner)
    ---
    delete:
      summary: Delete product
      tags: [Owner Products]
      security: [{Bearer: []}]
      parameters:
        - name: product_id
          in: path
          required: true
          type: integer
      responses:
        204:
          description: Deleted
    """
    product_service.delete_product(product_id, g.household_id)
    return "", 204


# =====================================================
# EMPLOYEE – F201 (READ ONLY)
# =====================================================

@employee_bp.route("", methods=["GET"])
@require_permission("F201", ["GET"])
def employee_list_products():
    """
    List products (Employee – read only)
    ---
    get:
      summary: List products
      tags: [Employee Products]
      security: [{Bearer: []}]
      responses:
        200:
          description: List of products
    """
    products = product_service.list_products(g.household_id)
    return jsonify([product_to_dict(p) for p in products]), 200


@employee_bp.route("/<int:product_id>", methods=["GET"])
@require_permission("F201", ["GET"])
def employee_get_product(product_id):
    """
    Get product by id (Employee – read only)
    ---
    get:
      summary: Get product
      tags: [Employee Products]
      security: [{Bearer: []}]
      parameters:
        - name: product_id
          in: path
          required: true
          type: integer
      responses:
        200:
          description: Product detail
        404:
          description: Not found
    """
    product = product_service.get_product(product_id, g.household_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    return jsonify(product_to_dict(product)), 200
