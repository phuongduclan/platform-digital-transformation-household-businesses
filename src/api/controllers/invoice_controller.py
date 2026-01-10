from flask import Blueprint, request, jsonify
from services.invoice_service import InvoiceService
from services.invoice_detail_service import InvoiceDetailService
from infrastructure.repositories.invoice_repository import InvoiceRepository
from infrastructure.repositories.invoice_detail_repository import InvoiceDetailRepository
from api.schemas.invoice import InvoiceRequestSchema, InvoiceResponseSchema, InvoiceWithDetailsSchema
from infrastructure.databases.factory_database import FactoryDatabase as db_factory

# Initialize services
invoice_service = InvoiceService(InvoiceRepository())
invoice_detail_service = InvoiceDetailService(InvoiceDetailRepository())

# Schemas
request_schema = InvoiceRequestSchema()
response_schema = InvoiceResponseSchema()
with_details_schema = InvoiceWithDetailsSchema()

# ============= OWNER BLUEPRINT =============
owner_invoice_bp = Blueprint('owner_invoice', __name__, url_prefix='/api/owner/invoices')

@owner_invoice_bp.route('/', methods=['GET'])
def list_all_invoices():
    """
    List all invoices (Owner only)
    ---
    get:
      summary: List all invoices
      tags:
        - Owner - Invoices
      responses:
        200:
          description: List of all invoices
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/InvoiceResponse'
    """
    invoices = invoice_service.list_all_invoices()
    return jsonify(response_schema.dump(invoices, many=True)), 200

@owner_invoice_bp.route('/', methods=['POST'])
def create_invoice():
    """
    Create invoice (Owner only)
    ---
    post:
      summary: Create a new invoice
      tags:
        - Owner - Invoices
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/InvoiceRequest'
      responses:
        201:
          description: Invoice created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/InvoiceResponse'
        400:
          description: Invalid input
    """
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    # TODO: Get user_id from JWT token
    user_id = 1  # Placeholder
    
    invoice = invoice_service.create_invoice(
        customer_name=data['customer_name'],
        total_amount=data.get('total_amount', 0.0),
        status=data.get('status', 'DRAFT'),
        source=data.get('source', 'MANUAL'),
        created_by=user_id
    )
    return jsonify(response_schema.dump(invoice)), 201

@owner_invoice_bp.route('/<int:invoice_id>', methods=['GET'])
def get_invoice(invoice_id):
    """
    Get invoice by id (Owner only)
    ---
    get:
      summary: Get invoice by ID
      tags:
        - Owner - Invoices
      parameters:
        - name: invoice_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        200:
          description: Invoice details
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/InvoiceResponse'
        404:
          description: Invoice not found
    """
    invoice = invoice_service.get_invoice(invoice_id)
    if not invoice:
        return jsonify({'message': 'Invoice not found'}), 404
    return jsonify(response_schema.dump(invoice)), 200

@owner_invoice_bp.route('/<int:invoice_id>', methods=['PUT'])
def update_invoice(invoice_id):
    """
    Update invoice (Owner only)
    ---
    put:
      summary: Update an invoice
      tags:
        - Owner - Invoices
      parameters:
        - name: invoice_id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/InvoiceRequest'
      responses:
        200:
          description: Invoice updated successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/InvoiceResponse'
        400:
          description: Invalid input
        404:
          description: Invoice not found
    """
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    try:
        invoice = invoice_service.update_invoice(
            invoice_id=invoice_id,
            customer_name=data['customer_name'],
            total_amount=data.get('total_amount', 0.0),
            status=data.get('status', 'DRAFT')
        )
        return jsonify(response_schema.dump(invoice)), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@owner_invoice_bp.route('/<int:invoice_id>', methods=['DELETE'])
def delete_invoice(invoice_id):
    """
    Delete invoice (Owner only)
    ---
    delete:
      summary: Delete an invoice
      tags:
        - Owner - Invoices
      parameters:
        - name: invoice_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        204:
          description: Invoice deleted successfully
        404:
          description: Invoice not found
    """
    try:
        invoice_service.delete_invoice(invoice_id)
        return '', 204
    except ValueError as e:
        return jsonify({'error': str(e)}), 404

@owner_invoice_bp.route('/<int:invoice_id>/details', methods=['GET'])
def get_invoice_with_details(invoice_id):
    """
    Get invoice with details (Owner only)
    ---
    get:
      summary: Get invoice with all details
      tags:
        - Owner - Invoices
      parameters:
        - name: invoice_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        200:
          description: Invoice with details
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/InvoiceWithDetails'
        404:
          description: Invoice not found
    """
    invoice = invoice_service.get_invoice(invoice_id)
    if not invoice:
        return jsonify({'message': 'Invoice not found'}), 404
    
    details = invoice_detail_service.list_invoice_details(invoice_id)
    
    # Combine invoice and details
    invoice_dict = response_schema.dump(invoice)
    invoice_dict['details'] = [
        {
            'id': d.id,
            'product_name': d.product_name,
            'quantity': d.quantity,
            'unit_price': d.unit_price,
            'subtotal': d.subtotal
        }
        for d in details
    ]
    
    return jsonify(invoice_dict), 200


# ============= EMPLOYEE BLUEPRINT =============
employee_invoice_bp = Blueprint('employee_invoice', __name__, url_prefix='/api/employee/invoices')

@employee_invoice_bp.route('/', methods=['POST'])
def create_draft_invoice():
    """
    Create draft invoice (Employee only)
    ---
    post:
      summary: Create a draft invoice
      tags:
        - Employee - Invoices
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/InvoiceRequest'
      responses:
        201:
          description: Draft invoice created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/InvoiceResponse'
        400:
          description: Invalid input
    """
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    # TODO: Get user_id from JWT token
    user_id = 2  # Placeholder for employee
    
    invoice = invoice_service.create_invoice(
        customer_name=data['customer_name'],
        total_amount=data.get('total_amount', 0.0),
        status='DRAFT',  # Force DRAFT for employees
        source='MANUAL',
        created_by=user_id
    )
    return jsonify(response_schema.dump(invoice)), 201

@employee_invoice_bp.route('/', methods=['GET'])
def list_own_invoices():
    """
    List own invoices (Employee only)
    ---
    get:
      summary: List invoices created by current employee
      tags:
        - Employee - Invoices
      responses:
        200:
          description: List of employee's invoices
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/InvoiceResponse'
    """
    # TODO: Get user_id from JWT token
    user_id = 2  # Placeholder for employee
    
    invoices = invoice_service.list_user_invoices(user_id)
    return jsonify(response_schema.dump(invoices, many=True)), 200

@employee_invoice_bp.route('/<int:invoice_id>', methods=['GET'])
def get_employee_invoice(invoice_id):
    """
    Get invoice by id (Employee only)
    ---
    get:
      summary: Get invoice by ID (own invoices only)
      tags:
        - Employee - Invoices
      parameters:
        - name: invoice_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        200:
          description: Invoice details
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/InvoiceResponse'
        403:
          description: Access denied
        404:
          description: Invoice not found
    """
    # TODO: Get user_id from JWT token and verify ownership
    invoice = invoice_service.get_invoice(invoice_id)
    if not invoice:
        return jsonify({'message': 'Invoice not found'}), 404
    
    return jsonify(response_schema.dump(invoice)), 200

@employee_invoice_bp.route('/<int:invoice_id>', methods=['PUT'])
def update_draft_invoice(invoice_id):
    """
    Update draft invoice (Employee only)
    ---
    put:
      summary: Update a draft invoice
      tags:
        - Employee - Invoices
      parameters:
        - name: invoice_id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/InvoiceRequest'
      responses:
        200:
          description: Invoice updated successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/InvoiceResponse'
        400:
          description: Invalid input or not a draft
        403:
          description: Access denied
        404:
          description: Invoice not found
    """
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    try:
        invoice = invoice_service.update_invoice(
            invoice_id=invoice_id,
            customer_name=data['customer_name'],
            total_amount=data.get('total_amount', 0.0),
            status='DRAFT'  # Keep as DRAFT
        )
        return jsonify(response_schema.dump(invoice)), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@employee_invoice_bp.route('/<int:invoice_id>/confirm', methods=['PUT'])
def confirm_invoice(invoice_id):
    """
    Confirm invoice (Employee only)
    ---
    put:
      summary: Confirm a draft invoice
      tags:
        - Employee - Invoices
      parameters:
        - name: invoice_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        200:
          description: Invoice confirmed successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/InvoiceResponse'
        400:
          description: Cannot confirm non-draft invoice
        403:
          description: Access denied
        404:
          description: Invoice not found
    """
    try:
        invoice = invoice_service.confirm_invoice(invoice_id)
        return jsonify(response_schema.dump(invoice)), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@employee_invoice_bp.route('/<int:invoice_id>/details', methods=['GET'])
def get_employee_invoice_details(invoice_id):
    """
    Get invoice details (Employee only)
    ---
    get:
      summary: Get invoice with all details
      tags:
        - Employee - Invoices
      parameters:
        - name: invoice_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        200:
          description: Invoice with details
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/InvoiceWithDetails'
        403:
          description: Access denied
        404:
          description: Invoice not found
    """
    invoice = invoice_service.get_invoice(invoice_id)
    if not invoice:
        return jsonify({'message': 'Invoice not found'}), 404
    
    details = invoice_detail_service.list_invoice_details(invoice_id)
    
    invoice_dict = response_schema.dump(invoice)
    invoice_dict['details'] = [
        {
            'id': d.id,
            'product_name': d.product_name,
            'quantity': d.quantity,
            'unit_price': d.unit_price,
            'subtotal': d.subtotal
        }
        for d in details
    ]
    
    return jsonify(invoice_dict), 200


# ============= DRAFT ORDER BLUEPRINT =============
draft_order_bp = Blueprint('draft_order', __name__, url_prefix='/api/employee/draft-orders')

@draft_order_bp.route('/', methods=['GET'])
def list_draft_orders():
    """
    View draft orders from AI (Employee only)
    ---
    get:
      summary: List draft orders created by AI
      tags:
        - Employee - Draft Orders
      responses:
        200:
          description: List of AI-generated draft orders
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/InvoiceResponse'
    """
    draft_orders = invoice_service.list_draft_orders()
    return jsonify(response_schema.dump(draft_orders, many=True)), 200

@draft_order_bp.route('/<int:invoice_id>/confirm', methods=['PUT'])
def confirm_draft_order(invoice_id):
    """
    Confirm draft order (Employee only)
    ---
    put:
      summary: Confirm an AI-generated draft order
      tags:
        - Employee - Draft Orders
      parameters:
        - name: invoice_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        200:
          description: Draft order confirmed successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/InvoiceResponse'
        400:
          description: Cannot confirm non-draft order
        404:
          description: Draft order not found
    """
    try:
        invoice = invoice_service.confirm_invoice(invoice_id)
        return jsonify(response_schema.dump(invoice)), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
