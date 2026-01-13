from flask import Blueprint, request, g, jsonify
from services.payment_service import PaymentService
from infrastructure.repositories.payment_repository import PaymentRepository
from infrastructure.repositories.invoice_repository import InvoiceRepository
from infrastructure.repositories.debt_record_repository import DebtRecordRepository
from infrastructure.repositories.accounting_ledger_repository import AccountingLedgerRepository
from infrastructure.repositories.customer_repository import CustomerRepository
from api.decorators.auth_decorators import require_permission
from api.schemas.payment import PaymentRequestSchema, PaymentUpdateSchema, PaymentResponseSchema
from decimal import Decimal

# =====================================================
# BLUEPRINTS
# =====================================================

owner_payment_bp = Blueprint(
    "owner_payments",
    __name__,
    url_prefix="/api/owner/payments"
)

employee_payment_bp = Blueprint(
    "employee_payments",
    __name__,
    url_prefix="/api/employee/payments"
)

# Initialize services
payment_repository = PaymentRepository()
invoice_repository = InvoiceRepository()
debt_record_repository = DebtRecordRepository()
accounting_ledger_repository = AccountingLedgerRepository()
customer_repository = CustomerRepository()

payment_service = PaymentService(
    payment_repository,
    invoice_repository,
    debt_record_repository,
    accounting_ledger_repository,
    customer_repository
)

# =====================================================
# HELPER FUNCTIONS
# =====================================================

def payment_to_dict(payment):
    return {
        "id": payment.id,
        "invoice_id": payment.invoice_id,
        "method_id": payment.method_id,
        "amount": str(payment.amount) if payment.amount else None,
        "description": payment.description,
        "status": payment.status,
        "created_by": payment.created_by,
        "updated_by": payment.updated_by,
        "created_at": payment.created_at.isoformat() if payment.created_at else None,
        "updated_at": payment.updated_at.isoformat() if payment.updated_at else None
    }

# =====================================================
# OWNER ENDPOINTS (F112)
# =====================================================

@owner_payment_bp.route("", methods=["GET"])
@require_permission("F112", ["GET"])
def owner_list_payments():
    """
    List payments (Owner)
    ---
    get:
      summary: List payments
      tags: [Owner Payments]
      security: [{Bearer: []}]
      parameters:
        - name: invoice_id
          in: query
          type: integer
        - name: customer_id
          in: query
          type: integer
      responses:
        200:
          description: List of payments
    """
    try:
        invoice_id = request.args.get('invoice_id', type=int)
        customer_id = request.args.get('customer_id', type=int)
        payments = payment_service.list_payments(
            g.household_id,
            invoice_id=invoice_id,
            customer_id=customer_id
        )
        return jsonify([payment_to_dict(p) for p in payments]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@owner_payment_bp.route("", methods=["POST"])
@require_permission("F112", ["POST"])
def owner_create_payment():
    """
    Create payment (Owner)
    Chỉ được tạo cho hóa đơn bán chịu (invoice_type = UNPAID) có khách hàng trong bảng customer.
    Tự động tạo DebtRecord (trả nợ) và AccountingLedger (thu tiền).
    ---
    post:
      summary: Create payment
      tags: [Owner Payments]
      security: [{Bearer: []}]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                invoice_id:
                  type: integer
                method_id:
                  type: integer
                amount:
                  type: number
                description:
                  type: string
      responses:
        201:
          description: Payment created
        400:
          description: Invalid request (hóa đơn không phải UNPAID hoặc không có customer_id)
    """
    data = request.get_json()
    schema = PaymentRequestSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify({"error": errors}), 400
    
    try:
        payment = payment_service.create_payment(
            invoice_id=data["invoice_id"],
            method_id=data["method_id"],
            amount=Decimal(str(data["amount"])),
            description=data.get("description"),
            created_by=str(g.user_id) if g.user_id else None,
            household_id=g.household_id
        )
        return jsonify(payment_to_dict(payment)), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@owner_payment_bp.route("/<int:payment_id>", methods=["GET"])
@require_permission("F112", ["GET"])
def owner_get_payment(payment_id):
    """
    Get payment by id (Owner)
    ---
    get:
      summary: Get payment
      tags: [Owner Payments]
      security: [{Bearer: []}]
      parameters:
        - name: payment_id
          in: path
          required: true
          type: integer
      responses:
        200:
          description: Payment detail
        404:
          description: Not found
    """
    payment = payment_service.get_payment(payment_id, g.household_id)
    if not payment:
        return jsonify({"error": "Payment not found"}), 404
    return jsonify(payment_to_dict(payment)), 200

@owner_payment_bp.route("/<int:payment_id>", methods=["PUT"])
@require_permission("F112", ["PUT"])
def owner_update_payment(payment_id):
    """
    Update payment (Owner)
    ---
    put:
      summary: Update payment
      tags: [Owner Payments]
      security: [{Bearer: []}]
      parameters:
        - name: payment_id
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
                method_id:
                  type: integer
                amount:
                  type: number
                description:
                  type: string
      responses:
        200:
          description: Payment updated
    """
    data = request.get_json()
    schema = PaymentUpdateSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify({"error": errors}), 400
    
    try:
        payment = payment_service.update_payment(
            payment_id=payment_id,
            household_id=g.household_id,
            method_id=data.get("method_id"),
            amount=Decimal(str(data["amount"])) if data.get("amount") else None,
            description=data.get("description"),
            updated_by=str(g.user_id) if g.user_id else None
        )
        return jsonify(payment_to_dict(payment)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@owner_payment_bp.route("/<int:payment_id>", methods=["DELETE"])
@require_permission("F112", ["DELETE"])
def owner_delete_payment(payment_id):
    """
    Delete payment (Owner)
    ---
    delete:
      summary: Delete payment
      tags: [Owner Payments]
      security: [{Bearer: []}]
      parameters:
        - name: payment_id
          in: path
          required: true
          type: integer
      responses:
        204:
          description: Deleted
    """
    try:
        payment_service.delete_payment(payment_id, g.household_id)
        return "", 204
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# =====================================================
# EMPLOYEE ENDPOINTS (F211)
# =====================================================

@employee_payment_bp.route("", methods=["POST"])
@require_permission("F211", ["POST"])
def employee_create_payment():
    """
    Record payment (Employee)
    Chỉ được tạo cho hóa đơn bán chịu (invoice_type = UNPAID) có khách hàng trong bảng customer.
    Tự động tạo DebtRecord (trả nợ) và AccountingLedger (thu tiền).
    ---
    post:
      summary: Record payment
      tags: [Employee Payments]
      security: [{Bearer: []}]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                invoice_id:
                  type: integer
                method_id:
                  type: integer
                amount:
                  type: number
                description:
                  type: string
      responses:
        201:
          description: Payment created
        400:
          description: Invalid request (hóa đơn không phải UNPAID hoặc không có customer_id)
    """
    data = request.get_json()
    schema = PaymentRequestSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify({"error": errors}), 400
    
    try:
        payment = payment_service.create_payment(
            invoice_id=data["invoice_id"],
            method_id=data["method_id"],
            amount=Decimal(str(data["amount"])),
            description=data.get("description"),
            created_by=str(g.user_id) if g.user_id else None,
            household_id=g.household_id
        )
        return jsonify(payment_to_dict(payment)), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@employee_payment_bp.route("/<int:payment_id>", methods=["GET"])
@require_permission("F211", ["GET"])
def employee_get_payment(payment_id):
    """
    Get payment by id (Employee)
    ---
    get:
      summary: Get payment
      tags: [Employee Payments]
      security: [{Bearer: []}]
      parameters:
        - name: payment_id
          in: path
          required: true
          type: integer
      responses:
        200:
          description: Payment detail
        404:
          description: Not found
    """
    payment = payment_service.get_payment(payment_id, g.household_id)
    if not payment:
        return jsonify({"error": "Payment not found"}), 404
    return jsonify(payment_to_dict(payment)), 200
