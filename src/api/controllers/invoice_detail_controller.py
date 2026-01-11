from flask import Blueprint, request, jsonify
from services.invoice_detail_service import InvoiceDetailService
from infrastructure.repositories.invoice_detail_repository import InvoiceDetailRepository
from api.schemas.invoice_detail import InvoiceDetailRequestSchema, InvoiceDetailResponseSchema
from api.decorators.auth_decorators import login_required

# Initialize service
invoice_detail_service = InvoiceDetailService(InvoiceDetailRepository())

# Schemas
request_schema = InvoiceDetailRequestSchema()
response_schema = InvoiceDetailResponseSchema()

# Blueprint
invoice_detail_bp = Blueprint('invoice_detail', __name__, url_prefix='/api/invoices')

@invoice_detail_bp.route('/<int:invoice_id>/details', methods=['GET'])
@login_required
def list_invoice_details(invoice_id):
    """
    List invoice details (Owner/Employee)
    ---
    get:
      summary: List all details for an invoice
      tags:
        - Invoice Details
      parameters:
        - name: invoice_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        200:
          description: List of invoice details
          content:
            application/json:
              schema:
                type: array
                items:
                  $ref: '#/components/schemas/InvoiceDetailResponse'
    """
    details = invoice_detail_service.list_invoice_details(invoice_id)
    return jsonify(response_schema.dump(details, many=True)), 200

@invoice_detail_bp.route('/<int:invoice_id>/details', methods=['POST'])
@login_required
def create_invoice_detail(invoice_id):
    """
    Create invoice detail (Owner/Employee)
    ---
    post:
      summary: Add a new item to an invoice
      tags:
        - Invoice Details
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
              $ref: '#/components/schemas/InvoiceDetailRequest'
      responses:
        201:
          description: Invoice detail created successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/InvoiceDetailResponse'
        400:
          description: Invalid input
    """
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    try:
        detail = invoice_detail_service.create_detail(
            invoice_id=invoice_id,
            product_name=data['product_name'],
            quantity=data['quantity'],
            unit_price=data['unit_price'],
            vat=data.get('vat', 0.0),
            discount=data.get('discount', 0.0),
            description=data.get('description')
        )
        return jsonify(response_schema.dump(detail)), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@invoice_detail_bp.route('/<int:invoice_id>/details/<int:detail_id>', methods=['GET'])
@login_required
def get_invoice_detail(invoice_id, detail_id):
    """
    Get invoice detail by id (Owner/Employee)
    ---
    get:
      summary: Get a specific invoice detail
      tags:
        - Invoice Details
      parameters:
        - name: invoice_id
          in: path
          required: true
          schema:
            type: integer
        - name: detail_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        200:
          description: Invoice detail
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/InvoiceDetailResponse'
        404:
          description: Invoice detail not found
    """
    detail = invoice_detail_service.get_detail(detail_id)
    if not detail:
        return jsonify({'message': 'Invoice detail not found'}), 404
    
    # Verify detail belongs to the invoice
    if detail.invoice_id != invoice_id:
        return jsonify({'message': 'Invoice detail not found'}), 404
    
    return jsonify(response_schema.dump(detail)), 200

@invoice_detail_bp.route('/<int:invoice_id>/details/<int:detail_id>', methods=['PUT'])
@login_required
def update_invoice_detail(invoice_id, detail_id):
    """
    Update invoice detail (Owner/Employee)
    ---
    put:
      summary: Update an invoice detail
      tags:
        - Invoice Details
      parameters:
        - name: invoice_id
          in: path
          required: true
          schema:
            type: integer
        - name: detail_id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/InvoiceDetailRequest'
      responses:
        200:
          description: Invoice detail updated successfully
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/InvoiceDetailResponse'
        400:
          description: Invalid input
        404:
          description: Invoice detail not found
    """
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    try:
        detail = invoice_detail_service.update_detail(
            detail_id=detail_id,
            product_name=data['product_name'],
            quantity=data['quantity'],
            unit_price=data['unit_price'],
            vat=data.get('vat', 0.0),
            discount=data.get('discount', 0.0),
            description=data.get('description')
        )
        return jsonify(response_schema.dump(detail)), 200
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@invoice_detail_bp.route('/<int:invoice_id>/details/<int:detail_id>', methods=['DELETE'])
@login_required
def delete_invoice_detail(invoice_id, detail_id):
    """
    Delete invoice detail (Owner/Employee)
    ---
    delete:
      summary: Delete an invoice detail
      tags:
        - Invoice Details
      parameters:
        - name: invoice_id
          in: path
          required: true
          schema:
            type: integer
        - name: detail_id
          in: path
          required: true
          schema:
            type: integer
      responses:
        204:
          description: Invoice detail deleted successfully
        404:
          description: Invoice detail not found
    """
    try:
        invoice_detail_service.delete_detail(detail_id)
        return '', 204
    except ValueError as e:
        return jsonify({'error': str(e)}), 404
