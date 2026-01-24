from flask import Blueprint, request, g, jsonify
from domain.models.iinvoice_service import IInvoiceService
from domain.models.iinvoice_detail_service import IInvoiceDetailService
from domain.models.iimport_receipt_service import IImportReceiptService
from domain.models.iexport_receipt_service import IExportReceiptService
from domain.models.iinventory_service import IInventoryService
from domain.models.idebt_record_service import IDebtRecordService
from domain.models.iaccounting_ledger_service import IAccountingLedgerService
from services.invoice_service import InvoiceService
from services.invoice_detail_service import InvoiceDetailService
from services.import_receipt_service import ImportReceiptService
from services.export_receipt_service import ExportReceiptService
from services.inventory_service import InventoryService
from services.debt_record_service import DebtRecordService
from services.accounting_ledger_service import AccountingLedgerService
from infrastructure.repositories.invoice_repository import InvoiceRepository
from infrastructure.repositories.invoice_detail_repository import InvoiceDetailRepository
from infrastructure.repositories.import_receipt_repository import ImportReceiptRepository
from infrastructure.repositories.export_receipt_repository import ExportReceiptRepository
from infrastructure.repositories.inventory_repository import InventoryRepository
from infrastructure.repositories.import_detail_repository import ImportDetailRepository
from infrastructure.repositories.export_detail_repository import ExportDetailRepository
from infrastructure.repositories.warehouse_repository import WarehouseRepository
from infrastructure.repositories.debt_record_repository import DebtRecordRepository
from infrastructure.repositories.accounting_ledger_repository import AccountingLedgerRepository
from infrastructure.repositories.customer_repository import CustomerRepository
from infrastructure.repositories.seller_repository import SellerRepository
from infrastructure.repositories.household_repository import HouseholdRepository
from infrastructure.repositories.product_repository import ProductRepository
from infrastructure.repositories.unit_repository import UnitRepository
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
invoice_service: IInvoiceService = InvoiceService(invoice_repository, invoice_detail_repository)
invoice_detail_service: IInvoiceDetailService = InvoiceDetailService(invoice_detail_repository, invoice_repository)

# Initialize import/export/inventory services for auto-creation
import_receipt_repository = ImportReceiptRepository()
import_detail_repository = ImportDetailRepository()
export_receipt_repository = ExportReceiptRepository()
export_detail_repository = ExportDetailRepository()
inventory_repository = InventoryRepository()
warehouse_repository = WarehouseRepository()
debt_record_repository = DebtRecordRepository()
accounting_ledger_repository = AccountingLedgerRepository()
customer_repository = CustomerRepository()
seller_repository = SellerRepository()
household_repository = HouseholdRepository()
product_repository = ProductRepository()
unit_repository = UnitRepository()

import_receipt_service: IImportReceiptService = ImportReceiptService(import_receipt_repository, import_detail_repository)
export_receipt_service: IExportReceiptService = ExportReceiptService(export_receipt_repository, export_detail_repository)
inventory_service: IInventoryService = InventoryService(inventory_repository)
debt_record_service: IDebtRecordService = DebtRecordService(debt_record_repository)
accounting_ledger_service: IAccountingLedgerService = AccountingLedgerService(accounting_ledger_repository)

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
    except (ValueError, Exception) as e:
        from api.utils.exception_handler import handle_exception_with_rollback
        return handle_exception_with_rollback(e, 400 if isinstance(e, ValueError) else 500)

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
        invoice = invoice_service.confirm_invoice(
            invoice_id, g.household_id, str(g.user_id) if g.user_id else None,
            import_receipt_service=import_receipt_service,
            export_receipt_service=export_receipt_service,
            inventory_service=inventory_service,
            warehouse_repository=warehouse_repository,
            debt_record_service=debt_record_service,
            accounting_ledger_service=accounting_ledger_service,
            seller_repository=seller_repository,
            customer_repository=customer_repository
        )
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
    Get invoice data for printing (Owner) - Returns JSON with all invoice data
    ---
    get:
      summary: Get invoice data for printing
      tags: [Owner Invoices]
      security: [{Bearer: []}]
      parameters:
        - name: invoice_id
          in: path
          required: true
          type: integer
      responses:
        200:
          description: Invoice data for printing (JSON)
    """
    invoice = invoice_service.get_invoice(invoice_id, g.household_id)
    if not invoice:
        return jsonify({"error": "Invoice not found"}), 404
    
    # Get invoice details
    details = invoice_detail_service.list_invoice_details(invoice_id, g.household_id)
    
    # Get household info
    household = household_repository.get_by_id(g.household_id)
    household_dict = None
    if household:
        household_dict = {
            "id": household.id,
            "name": household.name,
            "tax_code": household.tax_code,
            "address": household.address,
            "phone": household.phone,
            "description": household.description
        }
    
    # Get customer or seller
    customer_dict = None
    seller_dict = None
    if invoice.customer_id:
        customer = customer_repository.get_by_id(invoice.customer_id, g.household_id)
        if customer:
            customer_dict = {
                "id": customer.id,
                "name": customer.name,
                "tax_code": customer.tax_code,
                "address": customer.address,
                "phone": customer.phone
            }
    elif invoice.seller_id:
        seller = seller_repository.get_by_id(invoice.seller_id, g.household_id)
        if seller:
            seller_dict = {
                "id": seller.id,
                "name": seller.name,
                "tax_code": seller.tax_code,
                "address": seller.address,
                "phone": seller.phone
            }
    
    # Enrich details with product and unit names
    enriched_details = []
    for detail in details:
        product = product_repository.get_by_id(detail.product_id, g.household_id) if detail.product_id else None
        unit = unit_repository.get_by_id(detail.unit_id, g.household_id) if detail.unit_id else None
        detail_dict = invoice_detail_to_dict(detail)
        detail_dict['product_name'] = product.name if product else 'Sản phẩm'
        detail_dict['unit_name'] = unit.name if unit else ''
        # Calculate line total
        quantity = float(detail.quantity or 0)
        price = float(detail.price or 0)
        discount = float(detail.discount or 0)
        vat_rate = float(detail.vat or 0)
        subtotal = quantity * price
        discount_amount = subtotal * discount / 100
        after_discount = subtotal - discount_amount
        vat_amount = after_discount * vat_rate / 100
        line_total = after_discount + vat_amount
        detail_dict['line_total'] = str(line_total)
        enriched_details.append(detail_dict)
    
    # Return JSON with all data
    return jsonify({
        "invoice": invoice_to_dict(invoice),
        "household": household_dict,
        "customer": customer_dict,
        "seller": seller_dict,
        "details": enriched_details
    }), 200

# =====================================================
# EMPLOYEE INVOICE ENDPOINTS - F207, F208, F209, F210
# =====================================================

@employee_invoice_bp.route("", methods=["GET"])
@require_permission("F208", ["GET"])
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
@require_permission("F207", ["POST"])
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
    except (ValueError, Exception) as e:
        from api.utils.exception_handler import handle_exception_with_rollback
        return handle_exception_with_rollback(e, 400 if isinstance(e, ValueError) else 500)

@employee_invoice_bp.route("/<int:invoice_id>", methods=["GET"])
@require_permission("F208", ["GET"])
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
@require_permission("F213", ["DELETE"])
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
        invoice = invoice_service.confirm_invoice(
            invoice_id, g.household_id, str(g.user_id) if g.user_id else None,
            import_receipt_service=import_receipt_service,
            export_receipt_service=export_receipt_service,
            inventory_service=inventory_service,
            warehouse_repository=warehouse_repository,
            debt_record_service=debt_record_service,
            accounting_ledger_service=accounting_ledger_service,
            seller_repository=seller_repository,
            customer_repository=customer_repository
        )
        return jsonify(invoice_to_dict(invoice)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@employee_invoice_bp.route("/<int:invoice_id>/details", methods=["GET"])
@require_permission("F208", ["GET"])
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
@require_permission("F208", ["GET"])
def employee_print_invoice(invoice_id):
    """
    Get invoice data for printing (Employee) - Returns JSON with all invoice data
    ---
    get:
      summary: Get invoice data for printing
      tags: [Employee Invoices]
      security: [{Bearer: []}]
      parameters:
        - name: invoice_id
          in: path
          required: true
          type: integer
      responses:
        200:
          description: Invoice data for printing (JSON)
    """
    invoice = invoice_service.get_invoice(invoice_id, g.household_id)
    if not invoice:
        return jsonify({"error": "Invoice not found"}), 404
    
    # Get invoice details
    details = invoice_detail_service.list_invoice_details(invoice_id, g.household_id)
    
    # Get household info
    household = household_repository.get_by_id(g.household_id)
    household_dict = None
    if household:
        household_dict = {
            "id": household.id,
            "name": household.name,
            "tax_code": household.tax_code,
            "address": household.address,
            "phone": household.phone,
            "description": household.description
        }
    
    # Get customer or seller
    customer_dict = None
    seller_dict = None
    if invoice.customer_id:
        customer = customer_repository.get_by_id(invoice.customer_id, g.household_id)
        if customer:
            customer_dict = {
                "id": customer.id,
                "name": customer.name,
                "tax_code": customer.tax_code,
                "address": customer.address,
                "phone": customer.phone
            }
    elif invoice.seller_id:
        seller = seller_repository.get_by_id(invoice.seller_id, g.household_id)
        if seller:
            seller_dict = {
                "id": seller.id,
                "name": seller.name,
                "tax_code": seller.tax_code,
                "address": seller.address,
                "phone": seller.phone
            }
    
    # Enrich details with product and unit names
    enriched_details = []
    for detail in details:
        product = product_repository.get_by_id(detail.product_id, g.household_id) if detail.product_id else None
        unit = unit_repository.get_by_id(detail.unit_id, g.household_id) if detail.unit_id else None
        detail_dict = invoice_detail_to_dict(detail)
        detail_dict['product_name'] = product.name if product else 'Sản phẩm'
        detail_dict['unit_name'] = unit.name if unit else ''
        # Calculate line total
        quantity = float(detail.quantity or 0)
        price = float(detail.price or 0)
        discount = float(detail.discount or 0)
        vat_rate = float(detail.vat or 0)
        subtotal = quantity * price
        discount_amount = subtotal * discount / 100
        after_discount = subtotal - discount_amount
        vat_amount = after_discount * vat_rate / 100
        line_total = after_discount + vat_amount
        detail_dict['line_total'] = str(line_total)
        enriched_details.append(detail_dict)
    
    # Return JSON with all data
    return jsonify({
        "invoice": invoice_to_dict(invoice),
        "household": household_dict,
        "customer": customer_dict,
        "seller": seller_dict,
        "details": enriched_details
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
