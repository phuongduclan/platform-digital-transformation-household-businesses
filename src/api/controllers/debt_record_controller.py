from flask import Blueprint, request, g, jsonify
from domain.models.idebt_record_service import IDebtRecordService
from services.debt_record_service import DebtRecordService
from infrastructure.repositories.debt_record_repository import DebtRecordRepository
from api.decorators.auth_decorators import require_permission
from api.schemas.debt_record import DebtRecordResponseSchema
from decimal import Decimal

# =====================================================
# BLUEPRINTS
# =====================================================

owner_debt_record_bp = Blueprint(
    "owner_debt_records",
    __name__,
    url_prefix="/api/owner/debt-records"
)

employee_debt_record_bp = Blueprint(
    "employee_debt_records",
    __name__,
    url_prefix="/api/employee/debt-records"
)

# Initialize services
debt_record_repository = DebtRecordRepository()
debt_record_service: IDebtRecordService = DebtRecordService(debt_record_repository)

# =====================================================
# HELPER FUNCTIONS
# =====================================================

def debt_record_to_dict(dr):
    return {
        "id": dr.id,
        "customer_id": dr.customer_id,
        "invoice_id": dr.invoice_id,
        "payment_id": dr.payment_id,
        "debit_amount": str(dr.debit_amount) if dr.debit_amount else None,
        "credit_amount": str(dr.credit_amount) if dr.credit_amount else None,
        "balance": str(dr.balance) if dr.balance else None,
        "description": dr.description,
        "record_at": dr.record_at.isoformat() if dr.record_at else None
    }

# =====================================================
# OWNER ENDPOINTS (F114)
# =====================================================

@owner_debt_record_bp.route("", methods=["GET"])
@require_permission("F114", ["GET"])
def owner_list_debt_records():
    """
    List debt records (Owner)
    ---
    get:
      summary: List debt records
      tags: [Owner Debt Records]
      security: [{Bearer: []}]
      parameters:
        - name: customer_id
          in: query
          type: integer
      responses:
        200:
          description: List of debt records
    """
    try:
        customer_id = request.args.get('customer_id', type=int)
        debt_records = debt_record_service.list_debt_records(
            g.household_id,
            customer_id=customer_id
        )
        return jsonify([debt_record_to_dict(dr) for dr in debt_records]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@owner_debt_record_bp.route("/<int:debt_record_id>", methods=["GET"])
@require_permission("F114", ["GET"])
def owner_get_debt_record(debt_record_id):
    """
    Get debt record by id (Owner)
    ---
    get:
      summary: Get debt record
      tags: [Owner Debt Records]
      security: [{Bearer: []}]
      parameters:
        - name: debt_record_id
          in: path
          required: true
          type: integer
      responses:
        200:
          description: Debt record detail
        404:
          description: Not found
    """
    debt_record = debt_record_service.get_debt_record(debt_record_id, g.household_id)
    if not debt_record:
        return jsonify({"error": "Debt record not found"}), 404
    return jsonify(debt_record_to_dict(debt_record)), 200

@owner_debt_record_bp.route("/customer/<int:customer_id>", methods=["GET"])
@require_permission("F114", ["GET"])
def owner_get_customer_debt_records(customer_id):
    """
    Get debt records by customer (Owner)
    ---
    get:
      summary: Get customer debt records
      tags: [Owner Debt Records]
      security: [{Bearer: []}]
      parameters:
        - name: customer_id
          in: path
          required: true
          type: integer
      responses:
        200:
          description: Customer debt records with current balance
    """
    try:
        debt_records = debt_record_service.get_customer_debt_records(customer_id, g.household_id)
        balance = debt_record_service.get_customer_balance(customer_id, g.household_id)
        return jsonify({
            "customer_id": customer_id,
            "current_balance": str(balance),
            "debt_records": [debt_record_to_dict(dr) for dr in debt_records]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# =====================================================
# EMPLOYEE ENDPOINTS (F212 - Read-only)
# =====================================================

@employee_debt_record_bp.route("", methods=["GET"])
@require_permission("F212", ["GET"])
def employee_list_debt_records():
    """List debt records (Employee, read-only)"""
    try:
        customer_id = request.args.get('customer_id', type=int)
        debt_records = debt_record_service.list_debt_records(
            g.household_id,
            customer_id=customer_id
        )
        return jsonify([debt_record_to_dict(dr) for dr in debt_records]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@employee_debt_record_bp.route("/<int:debt_record_id>", methods=["GET"])
@require_permission("F212", ["GET"])
def employee_get_debt_record(debt_record_id):
    """Get debt record by id (Employee, read-only)"""
    debt_record = debt_record_service.get_debt_record(debt_record_id, g.household_id)
    if not debt_record:
        return jsonify({"error": "Debt record not found"}), 404
    return jsonify(debt_record_to_dict(debt_record)), 200

@employee_debt_record_bp.route("/customer/<int:customer_id>", methods=["GET"])
@require_permission("F212", ["GET"])
def employee_get_customer_debt_records(customer_id):
    """Get customer debt records (Employee, read-only)"""
    try:
        debt_records = debt_record_service.get_customer_debt_records(customer_id, g.household_id)
        balance = debt_record_service.get_customer_balance(customer_id, g.household_id)
        return jsonify({
            "customer_id": customer_id,
            "current_balance": str(balance),
            "debt_records": [debt_record_to_dict(dr) for dr in debt_records]
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
