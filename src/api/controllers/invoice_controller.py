from flask import Blueprint, request, g, jsonify
from services.invoice_service import InvoiceService
from services.invoice_detail_service import InvoiceDetailService
from infrastructure.repositories.invoice_repository import InvoiceRepository
from infrastructure.repositories.invoice_detail_repository import InvoiceDetailRepository
from api.decorators.auth_decorators import require_permission
from api.schemas.invoice import (
    InvoiceWithDetailsRequestSchema, InvoiceUpdateSchema,
    InvoiceResponseSchema, InvoiceListResponseSchema
)
from api.schemas.invoice_detail import (
    InvoiceDetailRequestSchema, InvoiceDetailUpdateSchema,
    InvoiceDetailResponseSchema, InvoiceDetailListResponseSchema
)
from decimal import Decimal

# =====================================================
# BLUEPRINTS
# =====================================================

owner_invoice_bp = Blueprint(
    "owner_invoices",
    __name__,
    url_prefix="/api/owner/invoices"
)

employee_invoice_bp = Blueprint(
    "employee_invoices",
    __name__,
    url_prefix="/api/employee/invoices"
)

invoice_detail_bp = Blueprint(
    "invoice_details",
    __name__,
    url_prefix="/api/invoices"
)

# Initialize services
invoice_repository = InvoiceRepository()
invoice_detail_repository = InvoiceDetailRepository()
invoice_service = InvoiceService(invoice_repository, invoice_detail_repository)
invoice_detail_service = InvoiceDetailService(invoice_detail_repository, invoice_repository)

# =====================================================
# HELPER FUNCTIONS
# =====================================================

def invoice_to_dict(invoice):
    return {
        "id": invoice.id,
        "household_id": invoice.household_id,
        "seller_id": invoice.seller_id,
        "customer_id": invoice.customer_id,
        "invoice_type": invoice.invoice_type,
        "discount_total": str(invoice.discount_total) if invoice.discount_total else None,
        "vat_total": str(invoice.vat_total) if invoice.vat_total else None,
        "total_amount": str(invoice.total_amount) if invoice.total_amount else None,
        "description": invoice.description,
        "status": invoice.status,
        "created_by": invoice.created_by,
        "updated_by": invoice.updated_by,
        "created_at": invoice.created_at.isoformat() if invoice.created_at else None,
        "updated_at": invoice.updated_at.isoformat() if invoice.updated_at else None,
    }

def invoice_detail_to_dict(detail):
    return {
        "id": detail.id,
        "invoice_id": detail.invoice_id,
        "product_id": detail.product_id,
        "unit_id": detail.unit_id,
        "vat": detail.vat,
        "discount": detail.discount,
        "price": str(detail.price) if detail.price else None,
        "description": detail.description,
        "quantity": detail.quantity,
        "status": detail.status,
        "created_at": detail.created_at.isoformat() if detail.created_at else None,
        "updated_at": detail.updated_at.isoformat() if detail.updated_at else None,
    }

# =====================================================
# OWNER INVOICE ENDPOINTS - F111
# =====================================================

@owner_invoice_bp.route("", methods=["GET"])
@require_permission("F111", ["GET"])
def owner_list_invoices():
    """
    List all invoices của household (Owner)
    ---
    get:
      summary: List invoices
      tags: [Owner Invoices]
      security: [{Bearer: []}]
      parameters:
        - name: status
          in: query
          required: false
          schema:
            type: string
            enum: [Draft, Confirm, Delete]
      responses:
        200:
          description: List of invoices
    """
    status = request.args.get('status')
    invoices = invoice_service.list_invoices(g.household_id, status)
    return jsonify([invoice_to_dict(inv) for inv in invoices]), 200

@owner_invoice_bp.route("", methods=["POST"])
@require_permission("F111", ["POST"])
def owner_create_invoice():
    """
    Create invoice với details (Owner)
    ---
    post:
      summary: Create invoice with details
      tags: [Owner Invoices]
      security: [{Bearer: []}]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - details
              properties:
                seller_id:
                  type: integer
                customer_id:
                  type: integer
                invoice_type:
                  type: string
                  enum: [PAID, UNPAID]
                description:
                  type: string
                status:
                  type: string
                  enum: [Draft, Confirm, Delete]
                details:
                  type: array
                  items:
                    type: object
                    required:
                      - product_id
                      - unit_id
                      - quantity
                      - price
                    properties:
                      product_id:
                        type: integer
                      unit_id:
                        type: integer
                      quantity:
                        type: integer
                      price:
                        type: number
                      vat:
                        type: integer
                      discount:
                        type: integer
                      description:
                        type: string
      responses:
        201:
          description: Invoice created
    """
    data = request.get_json()
    schema = InvoiceWithDetailsRequestSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify({"error": errors}), 400

    try:
        details = data.get("details", [])
        # Convert None hoặc 0 thành None để tránh Foreign Key constraint violation
        seller_id = data.get("seller_id")
        customer_id = data.get("customer_id")
        if seller_id == 0 or seller_id == '0':
            seller_id = None
        if customer_id == 0 or customer_id == '0':
            customer_id = None
        
        invoice = invoice_service.create_invoice_with_details(
            household_id=g.household_id,
            seller_id=seller_id,
            customer_id=customer_id,
            invoice_type=data.get("invoice_type", "PAID"),
            description=data.get("description"),
            status=data.get("status", "Draft"),
            created_by=str(g.user_id) if g.user_id else None,
            details=details
        )
        return jsonify(invoice_to_dict(invoice)), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@owner_invoice_bp.route("/<int:invoice_id>", methods=["GET"])
@require_permission("F111", ["GET"])
def owner_get_invoice(invoice_id):
    """
    Get invoice by id (Owner)
    ---
    get:
      summary: Get invoice
      tags: [Owner Invoices]
      security: [{Bearer: []}]
      parameters:
        - name: invoice_id
          in: path
          required: true
          type: integer
      responses:
        200:
          description: Invoice detail
        404:
          description: Not found
    """
    invoice = invoice_service.get_invoice(invoice_id, g.household_id)
    if not invoice:
        return jsonify({"error": "Invoice not found"}), 404
    return jsonify(invoice_to_dict(invoice)), 200

@owner_invoice_bp.route("/<int:invoice_id>", methods=["PUT"])
@require_permission("F111", ["PUT"])
def owner_update_invoice(invoice_id):
    """
    Update invoice (Owner)
    ---
    put:
      summary: Update invoice
      tags: [Owner Invoices]
      security: [{Bearer: []}]
      parameters:
        - name: invoice_id
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
                seller_id:
                  type: integer
                customer_id:
                  type: integer
                invoice_type:
                  type: string
                  enum: [PAID, UNPAID]
                description:
                  type: string
      responses:
        200:
          description: Invoice updated
        404:
          description: Not found
    """
    data = request.get_json()
    schema = InvoiceUpdateSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify({"error": errors}), 400

    try:
        # Convert None hoặc 0 thành None để tránh Foreign Key constraint violation
        seller_id = data.get("seller_id")
        customer_id = data.get("customer_id")
        if seller_id == 0 or seller_id == '0':
            seller_id = None
        if customer_id == 0 or customer_id == '0':
            customer_id = None
        
        invoice = invoice_service.update_invoice(
            invoice_id=invoice_id,
            household_id=g.household_id,
            seller_id=seller_id,
            customer_id=customer_id,
            invoice_type=data.get("invoice_type"),
            description=data.get("description"),
            updated_by=str(g.user_id) if g.user_id else None
        )
        return jsonify(invoice_to_dict(invoice)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@owner_invoice_bp.route("/<int:invoice_id>", methods=["DELETE"])
@require_permission("F111", ["DELETE"])
def owner_delete_invoice(invoice_id):
    """
    Delete invoice (Owner)
    ---
    delete:
      summary: Delete invoice
      tags: [Owner Invoices]
      security: [{Bearer: []}]
      parameters:
        - name: invoice_id
          in: path
          required: true
          type: integer
      responses:
        204:
          description: Deleted
    """
    try:
        invoice_service.delete_invoice(invoice_id, g.household_id)
        return "", 204
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@owner_invoice_bp.route("/<int:invoice_id>/confirm", methods=["PUT"])
@require_permission("F111", ["PUT"])
def owner_confirm_invoice(invoice_id):
    """
    Confirm invoice (Owner)
    ---
    put:
      summary: Confirm invoice
      tags: [Owner Invoices]
      security: [{Bearer: []}]
      parameters:
        - name: invoice_id
          in: path
          required: true
          type: integer
      responses:
        200:
          description: Invoice confirmed
        404:
          description: Not found
    """
    try:
        invoice = invoice_service.confirm_invoice(invoice_id, g.household_id, g.user_id)
        return jsonify(invoice_to_dict(invoice)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@owner_invoice_bp.route("/<int:invoice_id>/details", methods=["GET"])
@require_permission("F111", ["GET"])
def owner_get_invoice_details(invoice_id):
    """
    Get invoice details (Owner)
    ---
    get:
      summary: Get invoice details
      tags: [Owner Invoices]
      security: [{Bearer: []}]
      parameters:
        - name: invoice_id
          in: path
          required: true
          type: integer
      responses:
        200:
          description: List of invoice details
    """
    details = invoice_detail_service.list_invoice_details(invoice_id, g.household_id)
    return jsonify([invoice_detail_to_dict(d) for d in details]), 200

@owner_invoice_bp.route("/<int:invoice_id>/print", methods=["GET"])
@require_permission("F111", ["GET"])
def owner_print_invoice(invoice_id):
    """
    Print invoice (Owner)
    ---
    get:
      summary: Print invoice
      tags: [Owner Invoices]
      security: [{Bearer: []}]
      parameters:
        - name: invoice_id
          in: path
          required: true
          type: integer
      responses:
        200:
          description: Invoice with details for printing
    """
    invoice = invoice_service.get_invoice(invoice_id, g.household_id)
    if not invoice:
        return jsonify({"error": "Invoice not found"}), 404
    
    details = invoice_detail_service.list_invoice_details(invoice_id, g.household_id)
    return jsonify({
        "invoice": invoice_to_dict(invoice),
        "details": [invoice_detail_to_dict(d) for d in details]
    }), 200

# =====================================================
# EMPLOYEE INVOICE ENDPOINTS - F207, F208, F209, F210
# =====================================================

@employee_invoice_bp.route("", methods=["GET"])
@require_permission("F207", ["GET"])
def employee_list_invoices():
    """
    List all invoices của household (Employee)
    ---
    get:
      summary: List invoices
      tags: [Employee Invoices]
      security: [{Bearer: []}]
      parameters:
        - name: status
          in: query
          required: false
          schema:
            type: string
            enum: [Draft, Confirm, Delete]
      responses:
        200:
          description: List of invoices
    """
    status = request.args.get('status')
    invoices = invoice_service.list_invoices(g.household_id, status)
    return jsonify([invoice_to_dict(inv) for inv in invoices]), 200

@employee_invoice_bp.route("", methods=["POST"])
@require_permission("F208", ["POST"])
def employee_create_invoice():
    """
    Create draft invoice với details (Employee)
    ---
    post:
      summary: Create draft invoice with details
      tags: [Employee Invoices]
      security: [{Bearer: []}]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - details
              properties:
                seller_id:
                  type: integer
                customer_id:
                  type: integer
                invoice_type:
                  type: string
                  enum: [PAID, UNPAID]
                description:
                  type: string
                details:
                  type: array
                  items:
                    type: object
                    required:
                      - product_id
                      - unit_id
                      - quantity
                      - price
                    properties:
                      product_id:
                        type: integer
                      unit_id:
                        type: integer
                      quantity:
                        type: integer
                      price:
                        type: number
                      vat:
                        type: integer
                      discount:
                        type: integer
                      description:
                        type: string
      responses:
        201:
          description: Invoice created
    """
    data = request.get_json()
    schema = InvoiceWithDetailsRequestSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify({"error": errors}), 400

    try:
        details = data.get("details", [])
        # Convert None hoặc 0 thành None để tránh Foreign Key constraint violation
        seller_id = data.get("seller_id")
        customer_id = data.get("customer_id")
        if seller_id == 0 or seller_id == '0':
            seller_id = None
        if customer_id == 0 or customer_id == '0':
            customer_id = None
        
        # Employee luôn tạo với status='Draft'
        invoice = invoice_service.create_invoice_with_details(
            household_id=g.household_id,
            seller_id=seller_id,
            customer_id=customer_id,
            invoice_type=data.get("invoice_type", "PAID"),
            description=data.get("description"),
            status="Draft",  # Employee luôn tạo Draft
            created_by=str(g.user_id) if g.user_id else None,
            details=details
        )
        return jsonify(invoice_to_dict(invoice)), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@employee_invoice_bp.route("/<int:invoice_id>", methods=["GET"])
@require_permission("F207", ["GET"])
def employee_get_invoice(invoice_id):
    """
    Get invoice by id (Employee)
    ---
    get:
      summary: Get invoice
      tags: [Employee Invoices]
      security: [{Bearer: []}]
      parameters:
        - name: invoice_id
          in: path
          required: true
          type: integer
      responses:
        200:
          description: Invoice detail
        404:
          description: Not found
    """
    invoice = invoice_service.get_invoice(invoice_id, g.household_id)
    if not invoice:
        return jsonify({"error": "Invoice not found"}), 404
    return jsonify(invoice_to_dict(invoice)), 200

@employee_invoice_bp.route("/<int:invoice_id>", methods=["PUT"])
@require_permission("F209", ["PUT"])
def employee_update_invoice(invoice_id):
    """
    Update draft invoice (Employee)
    ---
    put:
      summary: Update draft invoice
      tags: [Employee Invoices]
      security: [{Bearer: []}]
      parameters:
        - name: invoice_id
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
                seller_id:
                  type: integer
                customer_id:
                  type: integer
                invoice_type:
                  type: string
                  enum: [PAID, UNPAID]
                description:
                  type: string
      responses:
        200:
          description: Invoice updated
        404:
          description: Not found
    """
    data = request.get_json()
    schema = InvoiceUpdateSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify({"error": errors}), 400

    try:
        # Convert None hoặc 0 thành None để tránh Foreign Key constraint violation
        seller_id = data.get("seller_id")
        customer_id = data.get("customer_id")
        if seller_id == 0 or seller_id == '0':
            seller_id = None
        if customer_id == 0 or customer_id == '0':
            customer_id = None
        
        invoice = invoice_service.update_invoice(
            invoice_id=invoice_id,
            household_id=g.household_id,
            seller_id=seller_id,
            customer_id=customer_id,
            invoice_type=data.get("invoice_type"),
            description=data.get("description"),
            updated_by=str(g.user_id) if g.user_id else None
        )
        return jsonify(invoice_to_dict(invoice)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@employee_invoice_bp.route("/<int:invoice_id>", methods=["DELETE"])
@require_permission("F209", ["DELETE"])
def employee_delete_invoice(invoice_id):
    """
    Delete draft invoice (Employee)
    ---
    delete:
      summary: Delete draft invoice
      tags: [Employee Invoices]
      security: [{Bearer: []}]
      parameters:
        - name: invoice_id
          in: path
          required: true
          type: integer
      responses:
        204:
          description: Deleted
    """
    try:
        invoice_service.delete_invoice(invoice_id, g.household_id)
        return "", 204
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@employee_invoice_bp.route("/<int:invoice_id>/confirm", methods=["PUT"])
@require_permission("F210", ["PUT"])
def employee_confirm_invoice(invoice_id):
    """
    Confirm invoice (Employee)
    ---
    put:
      summary: Confirm invoice
      tags: [Employee Invoices]
      security: [{Bearer: []}]
      parameters:
        - name: invoice_id
          in: path
          required: true
          type: integer
      responses:
        200:
          description: Invoice confirmed
        404:
          description: Not found
    """
    try:
        invoice = invoice_service.confirm_invoice(invoice_id, g.household_id, g.user_id)
        return jsonify(invoice_to_dict(invoice)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@employee_invoice_bp.route("/<int:invoice_id>/details", methods=["GET"])
@require_permission("F207", ["GET"])
def employee_get_invoice_details(invoice_id):
    """
    Get invoice details (Employee)
    ---
    get:
      summary: Get invoice details
      tags: [Employee Invoices]
      security: [{Bearer: []}]
      parameters:
        - name: invoice_id
          in: path
          required: true
          type: integer
      responses:
        200:
          description: List of invoice details
    """
    details = invoice_detail_service.list_invoice_details(invoice_id, g.household_id)
    return jsonify([invoice_detail_to_dict(d) for d in details]), 200

@employee_invoice_bp.route("/<int:invoice_id>/print", methods=["GET"])
@require_permission("F207", ["GET"])
def employee_print_invoice(invoice_id):
    """
    Print invoice (Employee)
    ---
    get:
      summary: Print invoice
      tags: [Employee Invoices]
      security: [{Bearer: []}]
      parameters:
        - name: invoice_id
          in: path
          required: true
          type: integer
      responses:
        200:
          description: Invoice with details for printing
    """
    invoice = invoice_service.get_invoice(invoice_id, g.household_id)
    if not invoice:
        return jsonify({"error": "Invoice not found"}), 404
    
    details = invoice_detail_service.list_invoice_details(invoice_id, g.household_id)
    return jsonify({
        "invoice": invoice_to_dict(invoice),
        "details": [invoice_detail_to_dict(d) for d in details]
    }), 200

# =====================================================
# INVOICE DETAIL ENDPOINTS (Owner/Employee)
# =====================================================

@invoice_detail_bp.route("/<int:invoice_id>/details", methods=["GET"])
@require_permission("F111", ["GET"])  # Owner
def list_invoice_details(invoice_id):
    """
    List invoice details
    ---
    get:
      summary: List invoice details
      tags: [Invoice Details]
      security: [{Bearer: []}]
      parameters:
        - name: invoice_id
          in: path
          required: true
          type: integer
      responses:
        200:
          description: List of invoice details
    """
    details = invoice_detail_service.list_invoice_details(invoice_id, g.household_id)
    return jsonify([invoice_detail_to_dict(d) for d in details]), 200

@invoice_detail_bp.route("/<int:invoice_id>/details", methods=["POST"])
@require_permission("F111", ["POST"])  # Owner
def create_invoice_detail(invoice_id):
    """
    Create invoice detail
    ---
    post:
      summary: Create invoice detail
      tags: [Invoice Details]
      security: [{Bearer: []}]
      parameters:
        - name: invoice_id
          in: path
          required: true
          type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - product_id
                - unit_id
                - quantity
                - price
              properties:
                product_id:
                  type: integer
                unit_id:
                  type: integer
                quantity:
                  type: integer
                price:
                  type: number
                vat:
                  type: integer
                discount:
                  type: integer
                description:
                  type: string
      responses:
        201:
          description: Invoice detail created
    """
    data = request.get_json()
    schema = InvoiceDetailRequestSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify({"error": errors}), 400

    try:
        detail = invoice_detail_service.create_invoice_detail(
            invoice_id=invoice_id,
            product_id=data["product_id"],
            unit_id=data["unit_id"],
            quantity=data["quantity"],
            price=Decimal(str(data["price"])),
            vat=data.get("vat", 0),
            discount=data.get("discount", 0),
            description=data.get("description"),
            status=data.get("status", "Draft"),
            household_id=g.household_id
        )
        return jsonify(invoice_detail_to_dict(detail)), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@invoice_detail_bp.route("/<int:invoice_id>/details/<int:detail_id>", methods=["GET"])
@require_permission("F111", ["GET"])  # Owner
def get_invoice_detail(invoice_id, detail_id):
    """
    Get invoice detail by id
    ---
    get:
      summary: Get invoice detail
      tags: [Invoice Details]
      security: [{Bearer: []}]
      parameters:
        - name: invoice_id
          in: path
          required: true
          type: integer
        - name: detail_id
          in: path
          required: true
          type: integer
      responses:
        200:
          description: Invoice detail
        404:
          description: Not found
    """
    detail = invoice_detail_service.get_invoice_detail(detail_id, g.household_id)
    if not detail:
        return jsonify({"error": "Invoice detail not found"}), 404
    return jsonify(invoice_detail_to_dict(detail)), 200

@invoice_detail_bp.route("/<int:invoice_id>/details/<int:detail_id>", methods=["PUT"])
@require_permission("F111", ["PUT"])  # Owner
def update_invoice_detail(invoice_id, detail_id):
    """
    Update invoice detail
    ---
    put:
      summary: Update invoice detail
      tags: [Invoice Details]
      security: [{Bearer: []}]
      parameters:
        - name: invoice_id
          in: path
          required: true
          type: integer
        - name: detail_id
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
                product_id:
                  type: integer
                unit_id:
                  type: integer
                quantity:
                  type: integer
                price:
                  type: number
                vat:
                  type: integer
                discount:
                  type: integer
                description:
                  type: string
      responses:
        200:
          description: Invoice detail updated
        404:
          description: Not found
    """
    data = request.get_json()
    schema = InvoiceDetailUpdateSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify({"error": errors}), 400

    try:
        detail = invoice_detail_service.update_invoice_detail(
            invoice_detail_id=detail_id,
            household_id=g.household_id,
            product_id=data.get("product_id"),
            unit_id=data.get("unit_id"),
            quantity=data.get("quantity"),
            price=Decimal(str(data["price"])) if data.get("price") else None,
            vat=data.get("vat"),
            discount=data.get("discount"),
            description=data.get("description")
        )
        return jsonify(invoice_detail_to_dict(detail)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@invoice_detail_bp.route("/<int:invoice_id>/details/<int:detail_id>", methods=["DELETE"])
@require_permission("F111", ["DELETE"])  # Owner
def delete_invoice_detail(invoice_id, detail_id):
    """
    Delete invoice detail
    ---
    delete:
      summary: Delete invoice detail
      tags: [Invoice Details]
      security: [{Bearer: []}]
      parameters:
        - name: invoice_id
          in: path
          required: true
          type: integer
        - name: detail_id
          in: path
          required: true
          type: integer
      responses:
        204:
          description: Deleted
    """
    try:
        invoice_detail_service.delete_invoice_detail(detail_id, g.household_id)
        return "", 204
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
