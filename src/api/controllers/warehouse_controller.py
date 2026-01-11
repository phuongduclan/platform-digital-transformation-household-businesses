from flask import Blueprint, request, g, jsonify
from services.warehouse_service import WarehouseService
from infrastructure.repositories.warehouse_repository import WarehouseRepository
from api.decorators.auth_decorators import require_permission

# =====================================================
# BLUEPRINTS
# =====================================================

owner_bp = Blueprint(
    "owner_warehouses",
    __name__,
    url_prefix="/api/owner/warehouses"
)

employee_bp = Blueprint(
    "employee_warehouses",
    __name__,
    url_prefix="/api/employee/warehouses"
)

warehouse_service = WarehouseService(WarehouseRepository())


# =====================================================
# HELPER
# =====================================================

def warehouse_to_dict(w):
    return {
        "id": w.id,
        "household_id": w.household_id,
        "name": w.name,
        "address": w.address,
        "description": w.description,
        "status": w.status,
        "created_at": w.created_at.isoformat() if w.created_at else None,
        "updated_at": w.updated_at.isoformat() if w.updated_at else None,
    }


# =====================================================
# OWNER – F107
# =====================================================

@owner_bp.route("", methods=["GET"])
@require_permission("F107", ["GET"])
def owner_list_warehouses():
    """
    List warehouses (Owner)
    ---
    get:
      summary: List warehouses
      tags: [Owner Warehouses]
      security: [{Bearer: []}]
      responses:
        200:
          description: List of warehouses
    """
    warehouses = warehouse_service.list_warehouses(g.household_id)
    return jsonify([warehouse_to_dict(w) for w in warehouses]), 200


@owner_bp.route("", methods=["POST"])
@require_permission("F107", ["POST"])
def owner_create_warehouse():
    """
    Create warehouse (Owner)
    ---
    post:
      summary: Create warehouse
      tags: [Owner Warehouses]
      security:
        - Bearer: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - name
                - address
              properties:
                name:
                  type: string
                address:
                  type: string
                description:
                  type: string
                status:
                  type: string
                  enum: [ACTIVE, INACTIVE]
      responses:
        201:
          description: Warehouse created
    """
    data = request.get_json()

    warehouse = warehouse_service.create_warehouse(
        household_id=g.household_id,
        name=data["name"],
        address=data["address"],
        description=data.get("description"),
        status=data.get("status", "ACTIVE")
    )

    return jsonify(warehouse_to_dict(warehouse)), 201


@owner_bp.route("/<int:warehouse_id>", methods=["GET"])
@require_permission("F107", ["GET"])
def owner_get_warehouse(warehouse_id):
    """
    Get warehouse by id (Owner)
    ---
    get:
      summary: Get warehouse
      tags: [Owner Warehouses]
      security: [{Bearer: []}]
      parameters:
        - name: warehouse_id
          in: path
          required: true
          type: integer
      responses:
        200:
          description: Warehouse detail
        404:
          description: Not found
    """
    warehouse = warehouse_service.get_warehouse(warehouse_id, g.household_id)
    if not warehouse:
        return jsonify({"error": "Warehouse not found"}), 404

    return jsonify(warehouse_to_dict(warehouse)), 200


@owner_bp.route("/<int:warehouse_id>", methods=["PUT"])
@require_permission("F107", ["PUT"])
def owner_update_warehouse(warehouse_id):
    """
    Update warehouse (Owner)
    ---
    put:
      summary: Update warehouse
      tags: [Owner Warehouses]
      security:
        - Bearer: []
      parameters:
        - name: warehouse_id
          in: path
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                name:
                  type: string
                address:
                  type: string
                description:
                  type: string
                status:
                  type: string
                  enum: [ACTIVE, INACTIVE]
      responses:
        200:
          description: Warehouse updated
        404:
          description: Not found
    """
    data = request.get_json()

    warehouse = warehouse_service.update_warehouse(
        warehouse_id=warehouse_id,
        household_id=g.household_id,
        name=data.get("name"),
        address=data.get("address"),
        description=data.get("description"),
        status=data.get("status")
    )

    return jsonify(warehouse_to_dict(warehouse)), 200


@owner_bp.route("/<int:warehouse_id>", methods=["DELETE"])
@require_permission("F107", ["DELETE"])
def owner_delete_warehouse(warehouse_id):
    """
    Delete warehouse (Owner)
    ---
    delete:
      summary: Delete warehouse
      tags: [Owner Warehouses]
      security: [{Bearer: []}]
      parameters:
        - name: warehouse_id
          in: path
          required: true
          type: integer
      responses:
        204:
          description: Deleted
    """
    warehouse_service.delete_warehouse(warehouse_id, g.household_id)
    return "", 204


# =====================================================
# EMPLOYEE – F216 (READ ONLY)
# =====================================================

@employee_bp.route("", methods=["GET"])
@require_permission("F216", ["GET"])
def employee_list_warehouses():
    """
    List warehouses (Employee – read only)
    ---
    get:
      summary: List warehouses
      tags: [Employee Warehouses]
      security: [{Bearer: []}]
      responses:
        200:
          description: List of warehouses
    """
    warehouses = warehouse_service.list_warehouses(g.household_id)
    return jsonify([warehouse_to_dict(w) for w in warehouses]), 200


@employee_bp.route("/<int:warehouse_id>", methods=["GET"])
@require_permission("F216", ["GET"])
def employee_get_warehouse(warehouse_id):
    """
    Get warehouse by id (Employee – read only)
    ---
    get:
      summary: Get warehouse
      tags: [Employee Warehouses]
      security: [{Bearer: []}]
      parameters:
        - name: warehouse_id
          in: path
          required: true
          type: integer
      responses:
        200:
          description: Warehouse detail
        404:
          description: Not found
    """
    warehouse = warehouse_service.get_warehouse(warehouse_id, g.household_id)
    if not warehouse:
        return jsonify({"error": "Warehouse not found"}), 404

    return jsonify(warehouse_to_dict(warehouse)), 200
