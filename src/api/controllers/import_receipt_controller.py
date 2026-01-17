from flask import Blueprint, request, g, jsonify
from domain.models.iimport_receipt_service import IImportReceiptService
from services.import_receipt_service import ImportReceiptService
from infrastructure.repositories.import_receipt_repository import ImportReceiptRepository
from infrastructure.repositories.import_detail_repository import ImportDetailRepository
from api.decorators.auth_decorators import require_permission
from datetime import date

# =====================================================
# BLUEPRINT
# =====================================================

owner_import_receipt_bp = Blueprint(
    "owner_import_receipts",
    __name__,
    url_prefix="/api/owner/import-receipts"
)

# Initialize services
import_receipt_repository = ImportReceiptRepository()
import_detail_repository = ImportDetailRepository()
import_receipt_service: IImportReceiptService = ImportReceiptService(import_receipt_repository, import_detail_repository)

# =====================================================
# HELPER FUNCTIONS
# =====================================================

def import_receipt_to_dict(import_receipt):
    return {
        "id": import_receipt.id,
        "warehouse_id": import_receipt.warehouse_id,
        "invoice_id": import_receipt.invoice_id,
        "import_date": import_receipt.import_date.isoformat() if import_receipt.import_date else None,
        "status": import_receipt.status,
        "created_at": import_receipt.created_at.isoformat() if import_receipt.created_at else None,
        "updated_at": import_receipt.updated_at.isoformat() if import_receipt.updated_at else None
    }

# =====================================================
# OWNER ENDPOINTS (F108: R, U only - no POST, DELETE)
# =====================================================

@owner_import_receipt_bp.route("", methods=["GET"])
@require_permission("F108", ["GET"])
def owner_list_import_receipts():
    """
    List import receipts (Owner)
    ---
    get:
      summary: List import receipts
      tags: [Owner Import Receipts]
      security: [{Bearer: []}]
      responses:
        200:
          description: List of import receipts
    """
    try:
        import_receipts = import_receipt_service.list_import_receipts(g.household_id)
        return jsonify([import_receipt_to_dict(ir) for ir in import_receipts]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@owner_import_receipt_bp.route("/<int:import_receipt_id>", methods=["GET"])
@require_permission("F108", ["GET"])
def owner_get_import_receipt(import_receipt_id):
    """
    Get import receipt by id (Owner)
    ---
    get:
      summary: Get import receipt
      tags: [Owner Import Receipts]
      security: [{Bearer: []}]
      parameters:
        - name: import_receipt_id
          in: path
          required: true
          type: integer
      responses:
        200:
          description: Import receipt detail
        404:
          description: Not found
    """
    import_receipt = import_receipt_service.get_import_receipt(import_receipt_id, g.household_id)
    if not import_receipt:
        return jsonify({"error": "Import receipt not found"}), 404
    return jsonify(import_receipt_to_dict(import_receipt)), 200

@owner_import_receipt_bp.route("/<int:import_receipt_id>", methods=["PUT"])
@require_permission("F108", ["PUT"])
def owner_update_import_receipt(import_receipt_id):
    """
    Update import receipt (Owner)
    Owner chỉ được điều chỉnh (warehouse_id, import_date)
    ---
    put:
      summary: Update import receipt
      tags: [Owner Import Receipts]
      security: [{Bearer: []}]
      parameters:
        - name: import_receipt_id
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
                warehouse_id:
                  type: integer
                import_date:
                  type: string
                  format: date
      responses:
        200:
          description: Import receipt updated
        400:
          description: Bad request
        404:
          description: Not found
    """
    try:
        data = request.get_json()
        warehouse_id = data.get('warehouse_id')
        import_date_str = data.get('import_date')
        
        import_date = None
        if import_date_str:
            import_date = date.fromisoformat(import_date_str)
        
        import_receipt = import_receipt_service.update_import_receipt(
            import_receipt_id, g.household_id,
            warehouse_id=warehouse_id,
            import_date=import_date
        )
        return jsonify(import_receipt_to_dict(import_receipt)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@owner_import_receipt_bp.route("/<int:import_receipt_id>/details", methods=["GET"])
@require_permission("F108", ["GET"])
def owner_get_import_receipt_details(import_receipt_id):
    """
    Get import receipt details (Owner)
    ---
    get:
      summary: Get import receipt details
      tags: [Owner Import Receipts]
      security: [{Bearer: []}]
      parameters:
        - name: import_receipt_id
          in: path
          required: true
          type: integer
      responses:
        200:
          description: List of import details
    """
    try:
        import_details = import_detail_repository.list_by_import_id(import_receipt_id, g.household_id)
        return jsonify([{
            "id": detail.id,
            "import_id": detail.import_id,
            "product_id": detail.product_id,
            "unit_id": detail.unit_id,
            "quantity": detail.quantity
        } for detail in import_details]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
