from flask import Blueprint, request, jsonify
from services.subscription_plan_service import SubscriptionPlanService
from infrastructure.repositories.subscription_plan_repository import SubscriptionPlanRepository
from api.schemas.subscription_plan import SubscriptionPlanRequestSchema, SubscriptionPlanResponseSchema
from api.decorators.auth_decorators import require_permission
from infrastructure.databases.mssql import session
from datetime import datetime, timezone

# Admin endpoints (F002: manage_subscription_plans)
admin_bp = Blueprint('admin_subscription_plan', __name__, url_prefix='/api/admin/subscription-plans')

# Public endpoint (không cần auth - Owner chọn plan khi đăng ký)
public_bp = Blueprint('public_subscription_plan', __name__, url_prefix='/api/public/subscription-plans')

service = SubscriptionPlanService(SubscriptionPlanRepository(session=session))
request_schema = SubscriptionPlanRequestSchema()
response_schema = SubscriptionPlanResponseSchema()

# ---------------- PUBLIC ENDPOINT (No auth required) ----------------
@public_bp.route('', methods=['GET'])
def list_plans_public():
    """
    List all subscription plans (Public - No auth required)
    Owner sử dụng endpoint này để chọn plan khi đăng ký
    ---
    get:
      summary: Get all subscription plans (Public)
      tags:
        - Public SubscriptionPlans
      responses:
        200:
          description: List of subscription plans
          content:
            application/json:
              schema:
                type: array
                items:
                  type: object
                  properties:
                    id:
                      type: integer
                      example: 1
                    name:
                      type: string
                      example: "Premium Plan"
                    price:
                      type: number
                      example: 150.0
                    billing_cycle:
                      type: string
                      example: "monthly"
                    description:
                      type: string
                      example: "Gói đăng ký cao cấp"
                    status:
                      type: string
                      example: "active"
                    created_at:
                      type: string
                      example: "2026-01-09T17:00:00Z"
                    updated_at:
                      type: string
                      example: "2026-01-09T17:00:00Z"
    """
    plans = service.list_plans()
    # Chỉ trả về plans có status = "active"
    active_plans = [plan for plan in plans if getattr(plan, 'status', '').lower() == 'active']
    return jsonify(response_schema.dump(active_plans, many=True)), 200

# ---------------- OWNER ENDPOINTS (F102: view_own_household - Read subscription plans để upgrade) ----------------
owner_bp = Blueprint('owner_subscription_plan', __name__, url_prefix='/api/owner/subscription-plans')

@owner_bp.route('', methods=['GET'])
@require_permission(function_code="F102", methods=["GET"])  # Owner xem subscription plans để upgrade (dùng F102)
def list_plans_owner():
    """
    List all active subscription plans (Owner only) - để Owner xem và chọn plan khi upgrade
    Business Logic: Owner xem subscription plans để upgrade subscription của household mình
    ---
    get:
      summary: Get all active subscription plans (Owner only - để upgrade subscription)
      security:
        - Bearer: []
      tags:
        - Owner SubscriptionPlans
      responses:
        200:
          description: List of active subscription plans (để Owner chọn khi upgrade)
          content:
            application/json:
              schema:
                type: array
                items:
                  type: object
                  properties:
                    id:
                      type: integer
                      example: 1
                    name:
                      type: string
                      example: "Premium Plan"
                    price:
                      type: number
                      example: 150.0
                    billing_cycle:
                      type: string
                      example: "monthly"
                    description:
                      type: string
                      example: "Gói đăng ký cao cấp"
                    status:
                      type: string
                      example: "active"
                    created_at:
                      type: string
                      example: "2026-01-09T17:00:00Z"
                    updated_at:
                      type: string
                      example: "2026-01-09T17:00:00Z"
    """
    # Owner xem subscription plans để upgrade - chỉ trả về active plans
    plans = service.list_plans()
    active_plans = [plan for plan in plans if getattr(plan, 'status', '').lower() == 'active']
    return jsonify(response_schema.dump(active_plans, many=True)), 200

# ---------------- ADMIN ENDPOINTS (F002: manage_subscription_plans) ----------------
@admin_bp.route('', methods=['GET'])
@require_permission(function_code="F002", methods=["GET"])
def list_plans():
    """
    List all subscription plans
    ---
    get:
      summary: Get all subscription plans
      tags:
        - SubscriptionPlans
      responses:
        200:
          description: List of subscription plans
          content:
            application/json:
              schema:
                type: array
                items:
                  type: object
                  properties:
                    id:
                      type: integer
                      example: 1
                    name:
                      type: string
                      example: "Premium Plan"
                    price:
                      type: number
                      example: 150.0
                    created_at:
                      type: string
                      example: "2026-01-09T17:00:00Z"
                    updated_at:
                      type: string
                      example: "2026-01-09T17:00:00Z"
    """
    plans = service.list_plans()
    return jsonify(response_schema.dump(plans, many=True)), 200

# ---------------- CREATE ----------------
@admin_bp.route('', methods=['POST'])
@require_permission(function_code="F002", methods=["POST"])
def create_plan():
    """
    Create a new subscription plan
    ---
    post:
      summary: Create a subscription plan
      tags:
        - SubscriptionPlans
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                name:
                  type: string
                  example: "Premium Plan"
                price:
                  type: number
                  example: 150.0
                status:
                  type: string
                  example: "active"
                user_id:
                  type: integer
                  example: 123
                billing_cycle:
                  type: string
                  example: "monthly"
                description:
                  type: string
                  example: "Gói đăng ký cao cấp"
      responses:
        201:
          description: Subscription plan created
          content:
            application/json:
              schema:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  name:
                    type: string
                    example: "Premium Plan"
                  price:
                    type: number
                    example: 150.0
                  status:
                    type: string
                    example: "active"
                  billing_cycle:
                    type: string
                    example: "monthly"
                  description:
                    type: string
                    example: "Gói đăng ký cao cấp"
                  created_at:
                    type: string
                    example: "2026-01-09T17:00:00Z"
                  updated_at:
                    type: string
                    example: "2026-01-09T17:00:00Z"
        400:
          description: Invalid input
    """

    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    now = datetime.now(timezone.utc)
    plan = service.create_plan(
        name=data['name'],
        price=data['price'],
        user_id=data['user_id'],
        billing_cycle=data.get('billing_cycle'),
        description=data.get('description'),
        status=data.get('status', 'active'),
        created_by=data.get('created_by'),
        updated_by=data.get('updated_by'),
        created_at=now,
        updated_at=now
    )
    return jsonify(response_schema.dump(plan)), 201

# ---------------- GET BY ID ----------------
@admin_bp.route('/<int:id>', methods=['GET'])
@require_permission(function_code="F002", methods=["GET"])
def get_plan(id):
    """
    Get subscription plan by ID
    ---
    get:
      summary: Get a subscription plan by ID
      tags:
        - SubscriptionPlans
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
          description: ID of the subscription plan
      responses:
        200:
          description: Subscription plan object
          content:
            application/json:
              schema:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  name:
                    type: string
                    example: "Premium Plan"
                  price:
                    type: number
                    example: 150.0
                  created_at:
                    type: string
                    example: "2026-01-09T17:00:00Z"
                  updated_at:
                    type: string
                    example: "2026-01-09T17:00:00Z"
        404:
          description: Plan not found
    """
    plan = service.get_plan(id)
    if not plan:
        return jsonify({'message': 'Subscription plan not found'}), 404
    return jsonify(response_schema.dump(plan)), 200

# ---------------- UPDATE ----------------
@admin_bp.route('/<int:id>', methods=['PUT'])
@require_permission(function_code="F002", methods=["PUT"])
def update_plan(id):
    """
    Update subscription plan by ID
    ---
    put:
      summary: Update a subscription plan
      tags:
        - SubscriptionPlans
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
          description: ID of the subscription plan
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                name:
                  type: string
                  example: "Premium Plan"
                price:
                  type: number
                  example: 150.0
      responses:
        200:
          description: Updated subscription plan
          content:
            application/json:
              schema:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  name:
                    type: string
                    example: "Premium Plan"
                  price:
                    type: number
                    example: 150.0
                  created_at:
                    type: string
                    example: "2026-01-09T17:00:00Z"
                  updated_at:
                    type: string
                    example: "2026-01-09T17:00:00Z"
        400:
          description: Invalid input
        404:
          description: Plan not found
    """
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    plan = service.update_plan(
        plan_id=id,
        name=data.get('name'),
        user_id=data.get('user_id'),
        billing_cycle=data.get('billing_cycle'),
        price=data.get('price'),
        description=data.get('description'),
        status=data.get('status'),
        created_by=data.get('created_by'),
        updated_by=data.get('updated_by'),
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    return jsonify(response_schema.dump(plan)), 200

# ---------------- DELETE ----------------
@admin_bp.route('/<int:id>', methods=['DELETE'])
@require_permission(function_code="F002", methods=["DELETE"])
def delete_plan(id):
    """
    Delete subscription plan by ID
    ---
    delete:
      summary: Delete a subscription plan
      tags:
        - SubscriptionPlans
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
          description: ID of the subscription plan
      responses:
        204:
          description: Subscription plan deleted successfully
        404:
          description: Plan not found
    """
    service.delete_plan(id)
    return '', 204
