from flask import Blueprint, request, g, jsonify
from services.customer_service import CustomerService
from infrastructure.repositories.customer_repository import CustomerRepository
from infrastructure.repositories.invoice_repository import InvoiceRepository
from infrastructure.repositories.debt_record_repository import DebtRecordRepository
from api.decorators.auth_decorators import require_permission 
from api.schemas.customer import CustomerRequestSchema, CustomerUpdateSchema, CustomerResponseSchema

# =====================================================
# BLUEPRINTS
# =====================================================

owner_customer_bp = Blueprint(
    "owner_customers",
    __name__,
    url_prefix="/api/owner/customers"
)

employee_customer_bp = Blueprint(
    "employee_customers",
    __name__,
    url_prefix="/api/employee/customers"
)

# Initialize services
customer_repository = CustomerRepository()
invoice_repository = InvoiceRepository()
debt_record_repository = DebtRecordRepository()

customer_service = CustomerService(
    customer_repository,
    invoice_repository,
    debt_record_repository
)

# =====================================================
# HELPER FUNCTIONS
# =====================================================

def customer_to_dict(customer):
    return {
        "id": customer.id,
        "household_id": customer.household_id,
        "tax_code": customer.tax_code,
        "name": customer.name,
        "phone": customer.phone,
        "address": customer.address,
        "description": customer.description,
        "status": customer.status,
        "created_by": customer.created_by,
        "updated_by": customer.updated_by,
        "created_at": customer.created_at.isoformat() if customer.created_at else None,
        "updated_at": customer.updated_at.isoformat() if customer.updated_at else None
    }

# =====================================================
# OWNER ENDPOINTS (F109)
# =====================================================

@owner_customer_bp.route("", methods=["GET"])
@require_permission("F109", ["GET"])
def owner_list_customers():
    """
    List customers (Owner)
    ---
    get:
      summary: List customers
      tags: [Owner Customers]
      security: [{Bearer: []}]
      parameters:
        - name: status
          in: query
          type: string
          enum: [Active, Inactive]
      responses:
        200:
          description: List of customers
    """
    try:
        status = request.args.get('status')
        customers = customer_service.list_customers(g.household_id, status=status)
        return jsonify([customer_to_dict(c) for c in customers]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@owner_customer_bp.route("", methods=["POST"])
@require_permission("F109", ["POST"])
def owner_create_customer():
    """
    Create customer (Owner)
    ---
    post:
      summary: Create customer
      tags: [Owner Customers]
      security: [{Bearer: []}]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                tax_code:
                  type: string
                name:
                  type: string
                phone:
                  type: string
                address:
                  type: string
                description:
                  type: string
                status:
                  type: string
                  enum: [Active, Inactive]
      responses:
        201:
          description: Customer created
    """
    data = request.get_json()
    schema = CustomerRequestSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify({"error": errors}), 400
    
    try:
        customer = customer_service.create_customer(
            household_id=g.household_id,
            tax_code=data.get("tax_code"),
            name=data["name"],
            phone=data.get("phone"),
            address=data.get("address"),
            description=data.get("description"),
            status=data.get("status", "Active"),
            created_by=str(g.user_id) if g.user_id else None
        )
        return jsonify(customer_to_dict(customer)), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@owner_customer_bp.route("/<int:customer_id>", methods=["GET"])
@require_permission("F109", ["GET"])
def owner_get_customer(customer_id):
    """
    Get customer by id (Owner)
    ---
    get:
      summary: Get customer
      tags: [Owner Customers]
      security: [{Bearer: []}]
      parameters:
        - name: customer_id
          in: path
          required: true
          type: integer
      responses:
        200:
          description: Customer detail
        404:
          description: Not found
    """
    customer = customer_service.get_customer(customer_id, g.household_id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    return jsonify(customer_to_dict(customer)), 200

@owner_customer_bp.route("/<int:customer_id>", methods=["PUT"])
@require_permission("F109", ["PUT"])
def owner_update_customer(customer_id):
    """
    Update customer (Owner)
    ---
    put:
      summary: Update customer
      tags: [Owner Customers]
      security: [{Bearer: []}]
      parameters:
        - name: customer_id
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
                tax_code:
                  type: string
                name:
                  type: string
                phone:
                  type: string
                address:
                  type: string
                description:
                  type: string
                status:
                  type: string
                  enum: [Active, Inactive]
      responses:
        200:
          description: Customer updated
    """
    data = request.get_json()
    schema = CustomerUpdateSchema()
    errors = schema.validate(data)
    if errors:
        return jsonify({"error": errors}), 400
    
    try:
        customer = customer_service.update_customer(
            customer_id=customer_id,
            household_id=g.household_id,
            tax_code=data.get("tax_code"),
            name=data.get("name"),
            phone=data.get("phone"),
            address=data.get("address"),
            description=data.get("description"),
            status=data.get("status"),
            updated_by=str(g.user_id) if g.user_id else None
        )
        return jsonify(customer_to_dict(customer)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@owner_customer_bp.route("/<int:customer_id>", methods=["DELETE"])
@require_permission("F109", ["DELETE"])
def owner_delete_customer(customer_id):
    """
    Delete customer (Owner)
    ---
    delete:
      summary: Delete customer
      tags: [Owner Customers]
      security: [{Bearer: []}]
      parameters:
        - name: customer_id
          in: path
          required: true
          type: integer
      responses:
        204:
          description: Deleted
    """
    try:
        customer_service.delete_customer(customer_id, g.household_id)
        return "", 204
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@owner_customer_bp.route("/<int:customer_id>/history", methods=["GET"])
@require_permission("F109", ["GET"])
def owner_get_customer_history(customer_id):
    """
    Get customer purchase history (Owner)
    ---
    get:
      summary: Get customer purchase history
      tags: [Owner Customers]
      security: [{Bearer: []}]
      parameters:
        - name: customer_id
          in: path
          required: true
          type: integer
      responses:
        200:
          description: Customer purchase history
    """
    try:
        history = customer_service.get_customer_purchase_history(customer_id, g.household_id)
        return jsonify({
            "customer_id": customer_id,
            "purchase_history": history
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@owner_customer_bp.route("/<int:customer_id>/debt", methods=["GET"])
@require_permission("F109", ["GET"])
def owner_get_customer_debt(customer_id):
    """
    Get customer outstanding debt (Owner)
    ---
    get:
      summary: Get customer debt
      tags: [Owner Customers]
      security: [{Bearer: []}]
      parameters:
        - name: customer_id
          in: path
          required: true
          type: integer
      responses:
        200:
          description: Customer debt information
    """
    try:
        debt_info = customer_service.get_customer_debt(customer_id, g.household_id)
        return jsonify(debt_info), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# =====================================================
# EMPLOYEE ENDPOINTS (F205, F206)
# =====================================================

@employee_customer_bp.route("", methods=["GET"])
@require_permission("F205", ["GET"])
def employee_list_customers():
    """
    List customers (Employee, read-only)
    ---
    get:
      summary: List customers
      tags: [Employee Customers]
      security: [{Bearer: []}]
      parameters:
        - name: status
          in: query
          type: string
          enum: [Active, Inactive]
      responses:
        200:
          description: List of customers
    """
    try:
        status = request.args.get('status')
        customers = customer_service.list_customers(g.household_id, status=status)
        return jsonify([customer_to_dict(c) for c in customers]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@employee_customer_bp.route("/<int:customer_id>", methods=["GET"])
@require_permission("F205", ["GET"])
def employee_get_customer(customer_id):
    """
    Get customer by id (Employee, read-only)
    ---
    get:
      summary: Get customer
      tags: [Employee Customers]
      security: [{Bearer: []}]
      parameters:
        - name: customer_id
          in: path
          required: true
          type: integer
      responses:
        200:
          description: Customer detail
        404:
          description: Not found
    """
    customer = customer_service.get_customer(customer_id, g.household_id)
    if not customer:
        return jsonify({"error": "Customer not found"}), 404
    return jsonify(customer_to_dict(customer)), 200

@employee_customer_bp.route("/<int:customer_id>/debt", methods=["GET"])
@require_permission("F206", ["GET"])
def employee_get_customer_debt(customer_id):
    """
    Get customer debt (Employee, read-only)
    ---
    get:
      summary: Get customer debt
      tags: [Employee Customers]
      security: [{Bearer: []}]
      parameters:
        - name: customer_id
          in: path
          required: true
          type: integer
      responses:
        200:
          description: Customer debt information
    """
    try:
        debt_info = customer_service.get_customer_debt(customer_id, g.household_id)
        return jsonify(debt_info), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
