from flask import Blueprint, request, g, jsonify
from services.accounting_ledger_service import AccountingLedgerService
from infrastructure.repositories.accounting_ledger_repository import AccountingLedgerRepository
from api.decorators.auth_decorators import require_permission
from api.schemas.accounting_ledger import AccountingLedgerResponseSchema, RevenueReportResponseSchema
from datetime import datetime

# =====================================================
# BLUEPRINTS
# =====================================================

owner_accounting_ledger_bp = Blueprint(
    "owner_accounting_ledgers",
    __name__,
    url_prefix="/api/owner/accounting-ledgers"
)

owner_reports_bp = Blueprint(
    "owner_reports",
    __name__,
    url_prefix="/api/owner/reports"
)

admin_accounting_ledger_bp = Blueprint(
    "admin_accounting_ledgers",
    __name__,
    url_prefix="/api/admin/accounting-ledgers"
)

# Initialize services
accounting_ledger_repository = AccountingLedgerRepository()
accounting_ledger_service = AccountingLedgerService(accounting_ledger_repository)

# =====================================================
# HELPER FUNCTIONS
# =====================================================

def accounting_ledger_to_dict(al):
    return {
        "id": al.id,
        "invoice_id": al.invoice_id,
        "transaction_date": al.transaction_date.isoformat() if al.transaction_date else None,
        "description": al.description,
        "debit_amount": str(al.debit_amount) if al.debit_amount else None,
        "credit_amount": str(al.credit_amount) if al.credit_amount else None,
        "balance": str(al.balance) if al.balance else None,
        "document_number": al.document_number,
        "movement_type": al.movement_type,
        "status": al.status,
        "created_at": al.created_at.isoformat() if al.created_at else None,
        "updated_at": al.updated_at.isoformat() if al.updated_at else None
    }

# =====================================================
# OWNER ENDPOINTS (F116, F117)
# =====================================================

@owner_accounting_ledger_bp.route("", methods=["GET"])
@require_permission("F116", ["GET"])
def owner_list_accounting_ledgers():
    """
    List accounting ledgers (Owner)
    ---
    get:
      summary: List accounting ledgers
      tags: [Owner Accounting Ledgers]
      security: [{Bearer: []}]
      parameters:
        - name: from_date
          in: query
          type: string
          format: date
        - name: to_date
          in: query
          type: string
          format: date
        - name: movement_type
          in: query
          type: string
          enum: [Thu, Chi]
      responses:
        200:
          description: List of accounting ledgers
    """
    try:
        from_date_str = request.args.get('from_date')
        to_date_str = request.args.get('to_date')
        movement_type = request.args.get('movement_type')
        
        from_date = datetime.fromisoformat(from_date_str) if from_date_str else None
        to_date = datetime.fromisoformat(to_date_str) if to_date_str else None
        
        accounting_ledgers = accounting_ledger_service.list_accounting_ledgers(
            g.household_id,
            from_date=from_date,
            to_date=to_date,
            movement_type=movement_type
        )
        return jsonify([accounting_ledger_to_dict(al) for al in accounting_ledgers]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@owner_accounting_ledger_bp.route("/<int:accounting_ledger_id>", methods=["GET"])
@require_permission("F116", ["GET"])
def owner_get_accounting_ledger(accounting_ledger_id):
    """Get accounting ledger by id (Owner)"""
    accounting_ledger = accounting_ledger_service.get_accounting_ledger(accounting_ledger_id, g.household_id)
    if not accounting_ledger:
        return jsonify({"error": "Accounting ledger not found"}), 404
    return jsonify(accounting_ledger_to_dict(accounting_ledger)), 200

@owner_reports_bp.route("/daily-revenue", methods=["GET"])
@require_permission("F117", ["GET"])
def owner_daily_revenue():
    """
    Daily revenue report (Owner)
    ---
    get:
      summary: Daily revenue report
      tags: [Owner Reports]
      security: [{Bearer: []}]
      parameters:
        - name: date
          in: query
          type: string
          format: date
          required: true
      responses:
        200:
          description: Daily revenue
    """
    try:
        date_str = request.args.get('date')
        if not date_str:
            return jsonify({"error": "date parameter is required"}), 400
        
        date = datetime.fromisoformat(date_str)
        revenue = accounting_ledger_service.get_daily_revenue(g.household_id, date)
        
        return jsonify({
            "date": date_str,
            "total_revenue": str(revenue)
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@owner_reports_bp.route("/monthly-revenue", methods=["GET"])
@require_permission("F117", ["GET"])
def owner_monthly_revenue():
    """
    Monthly revenue report (Owner)
    ---
    get:
      summary: Monthly revenue report
      tags: [Owner Reports]
      security: [{Bearer: []}]
      parameters:
        - name: month
          in: query
          type: integer
          required: true
        - name: year
          in: query
          type: integer
          required: true
      responses:
        200:
          description: Monthly revenue
    """
    try:
        month = request.args.get('month', type=int)
        year = request.args.get('year', type=int)
        
        if not month or not year:
            return jsonify({"error": "month and year parameters are required"}), 400
        
        revenue = accounting_ledger_service.get_monthly_revenue(g.household_id, month, year)
        
        return jsonify({
            "month": month,
            "year": year,
            "total_revenue": str(revenue)
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@owner_reports_bp.route("/outstanding-debt", methods=["GET"])
@require_permission("F117", ["GET"])
def owner_outstanding_debt():
    """
    Outstanding debt report (Owner)
    ---
    get:
      summary: Outstanding debt report
      tags: [Owner Reports]
      security: [{Bearer: []}]
      responses:
        200:
          description: Outstanding debt by customer
    """
    try:
        from services.debt_record_service import DebtRecordService
        from infrastructure.repositories.debt_record_repository import DebtRecordRepository
        
        debt_record_service = DebtRecordService(DebtRecordRepository())
        debt_records = debt_record_service.list_debt_records(g.household_id)
        
        # Group by customer and get latest balance
        customer_balances = {}
        for dr in debt_records:
            if dr.customer_id not in customer_balances:
                balance = debt_record_service.get_customer_balance(dr.customer_id, g.household_id)
                if balance > 0:  # Chỉ lấy customers có nợ
                    customer_balances[dr.customer_id] = {
                        "customer_id": dr.customer_id,
                        "balance": str(balance)
                    }
        
        # Sort by balance DESC
        result = sorted(customer_balances.values(), key=lambda x: float(x["balance"]), reverse=True)
        
        return jsonify({
            "outstanding_debts": result
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# =====================================================
# ADMIN ENDPOINTS (F007)
# =====================================================

@admin_accounting_ledger_bp.route("", methods=["GET"])
@require_permission("F007", ["GET"])
def admin_list_accounting_ledgers():
    """List all accounting ledgers (Admin)"""
    try:
        household_id = request.args.get('household_id', type=int)
        from_date_str = request.args.get('from_date')
        to_date_str = request.args.get('to_date')
        
        from_date = datetime.fromisoformat(from_date_str) if from_date_str else None
        to_date = datetime.fromisoformat(to_date_str) if to_date_str else None
        
        if household_id:
            accounting_ledgers = accounting_ledger_service.list_accounting_ledgers(
                household_id,
                from_date=from_date,
                to_date=to_date
            )
        else:
            # Admin có thể xem tất cả (cần implement method list_all nếu cần)
            accounting_ledgers = []
        
        return jsonify([accounting_ledger_to_dict(al) for al in accounting_ledgers]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
