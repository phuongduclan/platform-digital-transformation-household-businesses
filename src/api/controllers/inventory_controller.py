from flask import Blueprint, request, g, jsonify
from domain.models.iinventory_service import IInventoryService
from services.inventory_service import InventoryService
from infrastructure.repositories.inventory_repository import InventoryRepository
from api.decorators.auth_decorators import require_permission

# =====================================================
# BLUEPRINTS
# =====================================================

owner_inventory_bp = Blueprint(
    "owner_inventory",
    __name__,
    url_prefix="/api/owner/inventory"
)

employee_inventory_bp = Blueprint(
    "employee_inventory",
    __name__,
    url_prefix="/api/employee/inventory"
)

# Initialize services
inventory_repository = InventoryRepository()
inventory_service: IInventoryService = InventoryService(inventory_repository)

# =====================================================
# HELPER FUNCTIONS
# =====================================================

def inventory_to_dict(inventory):
    return {
        "id": inventory.id,
        "product_id": inventory.product_id,
        "unit_id": inventory.unit_id,
        "warehouse_id": inventory.warehouse_id,
        "quantity": inventory.quantity,
        "created_at": inventory.created_at.isoformat() if inventory.created_at else None,
        "updated_at": inventory.updated_at.isoformat() if inventory.updated_at else None
    }

# =====================================================
# OWNER ENDPOINTS (F106: R, U only - no POST, DELETE)
# =====================================================

@owner_inventory_bp.route("", methods=["GET"])
@require_permission("F106", ["GET"])
def owner_list_inventory():
    """
    List inventory (Owner)
    ---
    get:
      summary: List inventory
      tags: [Owner Inventory]
      security: [{Bearer: []}]
      parameters:
        - name: warehouse_id
          in: query
          type: integer
        - name: product_id
          in: query
          type: integer
        - name: unit_id
          in: query
          type: integer
      responses:
        200:
          description: List of inventory
    """
    try:
        warehouse_id = request.args.get('warehouse_id', type=int)
        product_id = request.args.get('product_id', type=int)
        unit_id = request.args.get('unit_id', type=int)
        inventory_list = inventory_service.list_inventory(
            g.household_id,
            warehouse_id=warehouse_id,
            product_id=product_id,
            unit_id=unit_id
        )
        return jsonify([inventory_to_dict(inv) for inv in inventory_list]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@owner_inventory_bp.route("/<int:product_id>/<int:warehouse_id>", methods=["GET"])
@require_permission("F106", ["GET"])
def owner_get_inventory(product_id, warehouse_id):
    """
    Get inventory by product and warehouse (Owner)
    ---
    get:
      summary: Get inventory
      tags: [Owner Inventory]
      security: [{Bearer: []}]
      parameters:
        - name: product_id
          in: path
          required: true
          type: integer
        - name: warehouse_id
          in: path
          required: true
          type: integer
        - name: unit_id
          in: query
          type: integer
          description: Optional - Filter by unit_id for precise inventory lookup
      responses:
        200:
          description: Inventory detail
        404:
          description: Not found
    """
    unit_id = request.args.get('unit_id', type=int)
    inventory = inventory_service.get_inventory(product_id, warehouse_id, g.household_id, unit_id=unit_id)
    if not inventory:
        return jsonify({"error": "Inventory not found"}), 404
    return jsonify(inventory_to_dict(inventory)), 200

@owner_inventory_bp.route("/<int:inventory_id>", methods=["PUT"])
@require_permission("F106", ["PUT"])
def owner_update_inventory(inventory_id):
    """
    Update inventory (Owner)
    Owner chỉ được điều chỉnh quantity nếu cần
    ---
    put:
      summary: Update inventory
      tags: [Owner Inventory]
      security: [{Bearer: []}]
      parameters:
        - name: inventory_id
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
                quantity:
                  type: integer
      responses:
        200:
          description: Inventory updated
        400:
          description: Bad request
        404:
          description: Not found
    """
    try:
        data = request.get_json()
        quantity = data.get('quantity')
        
        if quantity is None:
            return jsonify({"error": "quantity is required"}), 400
        
        inventory = inventory_service.update_inventory(inventory_id, quantity, g.household_id)
        return jsonify(inventory_to_dict(inventory)), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# =====================================================
# EMPLOYEE ENDPOINTS (F203: R only - read-only)
# =====================================================

@employee_inventory_bp.route("", methods=["GET"])
@require_permission("F203", ["GET"])
def employee_list_inventory():
    """
    List inventory (Employee, read-only)
    ---
    get:
      summary: List inventory
      tags: [Employee Inventory]
      security: [{Bearer: []}]
      parameters:
        - name: warehouse_id
          in: query
          type: integer
        - name: product_id
          in: query
          type: integer
        - name: unit_id
          in: query
          type: integer
      responses:
        200:
          description: List of inventory
    """
    try:
        warehouse_id = request.args.get('warehouse_id', type=int)
        product_id = request.args.get('product_id', type=int)
        unit_id = request.args.get('unit_id', type=int)
        inventory_list = inventory_service.list_inventory(
            g.household_id,
            warehouse_id=warehouse_id,
            product_id=product_id,
            unit_id=unit_id
        )
        return jsonify([inventory_to_dict(inv) for inv in inventory_list]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@employee_inventory_bp.route("/<int:product_id>/<int:warehouse_id>", methods=["GET"])
@require_permission("F203", ["GET"])
def employee_get_inventory(product_id, warehouse_id):
    """
    Get inventory by product and warehouse (Employee, read-only)
    ---
    get:
      summary: Get inventory
      tags: [Employee Inventory]
      security: [{Bearer: []}]
      parameters:
        - name: product_id
          in: path
          required: true
          type: integer
        - name: warehouse_id
          in: path
          required: true
          type: integer
        - name: unit_id
          in: query
          type: integer
          description: Optional - Filter by unit_id for precise inventory lookup
      responses:
        200:
          description: Inventory detail
        404:
          description: Not found
    """
    unit_id = request.args.get('unit_id', type=int)
    inventory = inventory_service.get_inventory(product_id, warehouse_id, g.household_id, unit_id=unit_id)
    if not inventory:
        return jsonify({"error": "Inventory not found"}), 404
    return jsonify(inventory_to_dict(inventory)), 200
