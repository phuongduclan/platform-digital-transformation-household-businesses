from flask import Blueprint, request, g, jsonify
from domain.models.iexport_receipt_service import IExportReceiptService
from services.export_receipt_service import ExportReceiptService
from infrastructure.repositories.export_receipt_repository import ExportReceiptRepository
from infrastructure.repositories.export_detail_repository import ExportDetailRepository
from api.decorators.auth_decorators import require_permission
from datetime import date

# =====================================================
# BLUEPRINT
# =====================================================

owner_export_receipt_bp = Blueprint(
    "owner_export_receipts",
    __name__,
    url_prefix="/api/owner/export-receipts"
)

# Initialize services
export_receipt_repository = ExportReceiptRepository()
export_detail_repository = ExportDetailRepository()
export_receipt_service: IExportReceiptService = ExportReceiptService(export_receipt_repository, export_detail_repository)

# =====================================================
# HELPER FUNCTIONS
# =====================================================

def export_receipt_to_dict(export_receipt):
    return {
        "id": export_receipt.id,
        "warehouse_id": export_receipt.warehouse_id,
        "invoice_id": export_receipt.invoice_id,
        "export_date": export_receipt.export_date.isoformat() if export_receipt.export_date else None,
        "reason": export_receipt.reason,
        "status": export_receipt.status,
        "created_at": export_receipt.created_at.isoformat() if export_receipt.created_at else None,
        "updated_at": export_receipt.updated_at.isoformat() if export_receipt.updated_at else None
    }

# =====================================================
# OWNER ENDPOINTS (F118: R, U only - no POST, DELETE)
# =====================================================

@owner_export_receipt_bp.route("", methods=["GET"])
@require_permission("F118", ["GET"])
def owner_list_export_receipts():
    """
    List export receipts (Owner)
    ---
    get:
      summary: List export receipts
      tags: [Owner Export Receipts]
      security: [{Bearer: []}]
      responses:
        200:
          description: List of export receipts
    """
    try:
        export_receipts = export_receipt_service.list_export_receipts(g.household_id)
        return jsonify([export_receipt_to_dict(er) for er in export_receipts]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@owner_export_receipt_bp.route("/<int:export_receipt_id>", methods=["GET"])
@require_permission("F118", ["GET"])
def owner_get_export_receipt(export_receipt_id):
    """
    Get export receipt by id (Owner)
    ---
    get:
      summary: Get export receipt
      tags: [Owner Export Receipts]
      security: [{Bearer: []}]
      parameters:
        - name: export_receipt_id
          in: path
          required: true
          type: integer
      responses:
        200:
          description: Export receipt detail
        404:
          description: Not found
    """
    export_receipt = export_receipt_service.get_export_receipt(export_receipt_id, g.household_id)
    if not export_receipt:
        return jsonify({"error": "Export receipt not found"}), 404
    return jsonify(export_receipt_to_dict(export_receipt)), 200

@owner_export_receipt_bp.route("/<int:export_receipt_id>", methods=["PUT"])
@require_permission("F118", ["PUT"])
def owner_update_export_receipt(export_receipt_id):
    """
    Update export receipt (Owner)
    Owner chỉ được điều chỉnh (warehouse_id, export_date, reason)
    ---
    put:
      summary: Update export receipt
      tags: [Owner Export Receipts]
      security: [{Bearer: []}]
      parameters:
        - name: export_receipt_id
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
                export_date:
                  type: string
                  format: date
                reason:
                  type: string
      responses:
        200:
          description: Export receipt updated
        400:
          description: Bad request
        404:
          description: Not found
    """
    try:
        data = request.get_json()
        warehouse_id = data.get('warehouse_id')
        export_date_str = data.get('export_date')
        reason = data.get('reason')
        
        export_date = None
        if export_date_str:
            export_date = date.fromisoformat(export_date_str)
        
        export_receipt = export_receipt_service.update_export_receipt(
            export_receipt_id, g.household_id,
            warehouse_id=warehouse_id,
            export_date=export_date,
            reason=reason
        )
        return jsonify(export_receipt_to_dict(export_receipt)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@owner_export_receipt_bp.route("/<int:export_receipt_id>/details", methods=["GET"])
@require_permission("F118", ["GET"])
def owner_get_export_receipt_details(export_receipt_id):
    """
    Get export receipt details (Owner)
    ---
    get:
      summary: Get export receipt details
      tags: [Owner Export Receipts]
      security: [{Bearer: []}]
      parameters:
        - name: export_receipt_id
          in: path
          required: true
          type: integer
      responses:
        200:
          description: List of export details
    """
    try:
        export_details = export_detail_repository.list_by_export_id(export_receipt_id, g.household_id)
        return jsonify([{
            "id": detail.id,
            "export_id": detail.export_id,
            "product_id": detail.product_id,
            "unit_id": detail.unit_id,
            "quantity": detail.quantity
        } for detail in export_details]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
