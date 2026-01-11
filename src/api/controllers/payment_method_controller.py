from flask import Blueprint, request, g, jsonify
from services.payment_method_service import PaymentMethodService
from infrastructure.repositories.payment_method_repository import PaymentMethodRepository
from api.decorators.auth_decorators import require_permission
from api.schemas.payment_method import PaymentMethodRequestSchema, PaymentMethodResponseSchema

# =====================================================
# BLUEPRINTS
# =====================================================

owner_payment_method_bp = Blueprint(
    "owner_payment_methods",
    __name__,
    url_prefix="/api/owner/payment-methods"
)

admin_payment_method_bp = Blueprint(
    "admin_payment_methods",
    __name__,
    url_prefix="/api/admin/payment-methods"
)

# Initialize services
payment_method_repository = PaymentMethodRepository()
payment_method_service = PaymentMethodService(payment_method_repository)

# =====================================================
# HELPER FUNCTIONS
# =====================================================

def payment_method_to_dict(pm):
    return {
        "id": pm.id,
        "name": pm.name,
        "status": pm.status,
        "created_at": pm.created_at.isoformat() if pm.created_at else None,
        "updated_at": pm.updated_at.isoformat() if pm.updated_at else None
    }

# =====================================================
# OWNER ENDPOINTS (F113 - Read-only)
# =====================================================

@owner_payment_method_bp.route("", methods=["GET"])
@require_permission("F113", ["GET"])
def owner_list_payment_methods():
    """
    List payment methods (Owner, read-only)
    ---
    get:
      summary: List payment methods
      tags: [Owner Payment Methods]
      security: [{Bearer: []}]
      responses:
        200:
          description: List of payment methods
    """
    try:
        payment_methods = payment_method_service.list_payment_methods(status='Active')
        return jsonify([payment_method_to_dict(pm) for pm in payment_methods]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@owner_payment_method_bp.route("/<int:payment_method_id>", methods=["GET"])
@require_permission("F113", ["GET"])
def owner_get_payment_method(payment_method_id):
    """
    Get payment method by id (Owner, read-only)
    ---
    get:
      summary: Get payment method
      tags: [Owner Payment Methods]
      security: [{Bearer: []}]
      parameters:
        - name: payment_method_id
          in: path
          required: true
          type: integer
      responses:
        200:
          description: Payment method detail
        404:
          description: Not found
    """
    payment_method = payment_method_service.get_payment_method(payment_method_id)
    if not payment_method:
        return jsonify({"error": "Payment method not found"}), 404
    return jsonify(payment_method_to_dict(payment_method)), 200

# =====================================================
# ADMIN ENDPOINTS (F0xx - CRUD)
# =====================================================

@admin_payment_method_bp.route("", methods=["GET"])
@require_permission("F002", ["GET"])  # Admin manage system
def admin_list_payment_methods():
    """List all payment methods (Admin)"""
    try:
        payment_methods = payment_method_service.list_payment_methods()
        return jsonify([payment_method_to_dict(pm) for pm in payment_methods]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_payment_method_bp.route("", methods=["POST"])
@require_permission("F002", ["POST"])
def admin_create_payment_method():
    """Create payment method (Admin)"""
    data = request.get_json()
    schema = PaymentMethodRequestSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify({"error": errors}), 400
    
    try:
        payment_method = payment_method_service.create_payment_method(
            name=data["name"],
            status=data.get("status", "Active")
        )
        return jsonify(payment_method_to_dict(payment_method)), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_payment_method_bp.route("/<int:payment_method_id>", methods=["PUT"])
@require_permission("F002", ["PUT"])
def admin_update_payment_method(payment_method_id):
    """Update payment method (Admin)"""
    data = request.get_json()
    try:
        payment_method = payment_method_service.update_payment_method(
            payment_method_id=payment_method_id,
            name=data.get("name"),
            status=data.get("status")
        )
        return jsonify(payment_method_to_dict(payment_method)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@admin_payment_method_bp.route("/<int:payment_method_id>", methods=["DELETE"])
@require_permission("F002", ["DELETE"])
def admin_delete_payment_method(payment_method_id):
    """Delete payment method (Admin)"""
    try:
        payment_method_service.delete_payment_method(payment_method_id)
        return "", 204
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
