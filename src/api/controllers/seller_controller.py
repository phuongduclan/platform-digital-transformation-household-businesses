from flask import Blueprint, request, g, jsonify
from domain.models.iseller_service import ISellerService
from services.seller_service import SellerService
from infrastructure.repositories.seller_repository import SellerRepository
from api.decorators.auth_decorators import require_permission
from api.schemas.seller import SellerRequestSchema, SellerUpdateSchema, SellerResponseSchema

# =====================================================
# BLUEPRINTS
# =====================================================

owner_seller_bp = Blueprint(
    "owner_sellers",
    __name__,
    url_prefix="/api/owner/sellers"
)

# Initialize services
seller_repository = SellerRepository()
seller_service: ISellerService = SellerService(seller_repository)

# =====================================================
# HELPER FUNCTIONS
# =====================================================

def seller_to_dict(seller):
    return {
        "id": seller.id,
        "household_id": seller.household_id,
        "tax_code": seller.tax_code,
        "name": seller.name,
        "phone": seller.phone,
        "address": seller.address,
        "description": seller.description,
        "status": seller.status,
        "created_by": seller.created_by,
        "updated_by": seller.updated_by,
        "created_at": seller.created_at.isoformat() if seller.created_at else None,
        "updated_at": seller.updated_at.isoformat() if seller.updated_at else None
    }

# =====================================================
# OWNER ENDPOINTS (F110)
# =====================================================

@owner_seller_bp.route("", methods=["GET"])
@require_permission("F110", ["GET"])
def owner_list_sellers():
    """
    List sellers (Owner)
    ---
    get:
      summary: List sellers
      tags: [Owner Sellers]
      security: [{Bearer: []}]
      parameters:
        - name: status
          in: query
          type: string
          enum: [Active, Inactive]
      responses:
        200:
          description: List of sellers
    """
    try:
        status = request.args.get('status')
        sellers = seller_service.list_sellers(g.household_id, status=status)
        return jsonify([seller_to_dict(s) for s in sellers]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@owner_seller_bp.route("", methods=["POST"])
@require_permission("F110", ["POST"])
def owner_create_seller():
    """
    Create seller (Owner)
    ---
    post:
      summary: Create seller
      tags: [Owner Sellers]
      security: [{Bearer: []}]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                tax_code:
                  type: string
                name:
                  type: string
                phone:
                  type: string
                address:
                  type: string
                description:
                  type: string
                status:
                  type: string
                  enum: [Active, Inactive]
      responses:
        201:
          description: Seller created
    """
    data = request.get_json()
    schema = SellerRequestSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify({"error": errors}), 400
    
    try:
        seller = seller_service.create_seller(
            household_id=g.household_id,
            tax_code=data.get("tax_code"),
            name=data["name"],
            phone=data.get("phone"),
            address=data.get("address"),
            description=data.get("description"),
            status=data.get("status", "Active"),
            created_by=str(g.user_id) if g.user_id else None
        )
        return jsonify(seller_to_dict(seller)), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@owner_seller_bp.route("/<int:seller_id>", methods=["GET"])
@require_permission("F110", ["GET"])
def owner_get_seller(seller_id):
    """
    Get seller by id (Owner)
    ---
    get:
      summary: Get seller
      tags: [Owner Sellers]
      security: [{Bearer: []}]
      parameters:
        - name: seller_id
          in: path
          required: true
          type: integer
      responses:
        200:
          description: Seller detail
        404:
          description: Not found
    """
    seller = seller_service.get_seller(seller_id, g.household_id)
    if not seller:
        return jsonify({"error": "Seller not found"}), 404
    return jsonify(seller_to_dict(seller)), 200

@owner_seller_bp.route("/<int:seller_id>", methods=["PUT"])
@require_permission("F110", ["PUT"])
def owner_update_seller(seller_id):
    """
    Update seller (Owner)
    ---
    put:
      summary: Update seller
      tags: [Owner Sellers]
      security: [{Bearer: []}]
      parameters:
        - name: seller_id
          in: path
          required: true
          type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                tax_code:
                  type: string
                name:
                  type: string
                phone:
                  type: string
                address:
                  type: string
                description:
                  type: string
                status:
                  type: string
                  enum: [Active, Inactive]
      responses:
        200:
          description: Seller updated
    """
    data = request.get_json()
    schema = SellerUpdateSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify({"error": errors}), 400
    
    try:
        seller = seller_service.update_seller(
            seller_id=seller_id,
            household_id=g.household_id,
            tax_code=data.get("tax_code"),
            name=data.get("name"),
            phone=data.get("phone"),
            address=data.get("address"),
            description=data.get("description"),
            status=data.get("status"),
            updated_by=str(g.user_id) if g.user_id else None
        )
        return jsonify(seller_to_dict(seller)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@owner_seller_bp.route("/<int:seller_id>", methods=["DELETE"])
@require_permission("F110", ["DELETE"])
def owner_delete_seller(seller_id):
    """
    Delete seller (Owner)
    ---
    delete:
      summary: Delete seller
      tags: [Owner Sellers]
      security: [{Bearer: []}]
      parameters:
        - name: seller_id
          in: path
          required: true
          type: integer
      responses:
        204:
          description: Deleted
    """
    try:
        seller_service.delete_seller(seller_id, g.household_id)
        return "", 204
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
