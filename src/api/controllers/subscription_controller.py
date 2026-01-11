from flask import Blueprint, request, jsonify
from services.subscription_service import SubscriptionService
from infrastructure.repositories.subscription_repository import SubscriptionRepository
from api.schemas.subscription import SubscriptionRequestSchema, SubscriptionResponseSchema
from api.decorators.auth_decorators import require_permission
from api.utils.auth_utils import get_current_household_id
from infrastructure.databases.mssql import session
from datetime import datetime, timezone, timedelta

# Admin endpoints
admin_bp = Blueprint('admin_subscription', __name__, url_prefix='/api/admin/subscriptions')

# Owner endpoints
owner_bp = Blueprint('owner_subscription', __name__, url_prefix='/api/owner/subscription')

service = SubscriptionService(session)
request_schema = SubscriptionRequestSchema()
response_schema = SubscriptionResponseSchema()


# ---------------- OWNER ENDPOINTS (Owner tự quản lý subscription của mình) ----------------
@owner_bp.route('', methods=['GET'])
@require_permission(function_code="F102", methods=["GET"])  # Dùng F102 vì Owner quản lý subscription như một phần của household
def get_own_subscription():
    """
    Get own subscription (Owner only)
    Owner tự xem subscription của household mình
    ---
    get:
      summary: Get subscription of current owner's household
      security:
        - Bearer: []
      tags:
        - Owner Subscription
      responses:
        200:
          description: Subscription object
          content:
            application/json:
              schema:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  plan_id:
                    type: integer
                    example: 2
                  household_id:
                    type: integer
                    example: 3
                  start_date:
                    type: string
                    example: "2026-01-09T17:00:00Z"
                  end_date:
                    type: string
                    example: "2026-02-09T17:00:00Z"
                  is_active:
                    type: boolean
                    example: true
        400:
          description: Household ID is required
        404:
          description: Subscription not found
    """
    # Lấy household_id từ JWT token (tự động từ decorator)
    household_id = get_current_household_id()
    if not household_id:
        return jsonify({'error': 'Household ID is required'}), 400
    
    try:
        # Data isolation: Owner chỉ xem subscription của household mình
        subscription = service.get_own_subscription(household_id)
        if not subscription:
            return jsonify({'message': 'No active subscription found for your household'}), 404
        return jsonify(response_schema.dump(subscription)), 200
    except ValueError as e:
        if 'not found' in str(e).lower():
            return jsonify({'error': str(e)}), 404
        return jsonify({'error': str(e)}), 400


@owner_bp.route('', methods=['PUT'])
@require_permission(function_code="F102", methods=["PUT"])  # Dùng F102 vì Owner quản lý subscription như một phần của household
def upgrade_own_subscription():
    """
    Upgrade subscription plan (Owner only)
    Owner tự update subscription của household mình (upgrade plan)
    ---
    put:
      summary: Upgrade subscription plan for current owner's household
      security:
        - Bearer: []
      tags:
        - Owner Subscription
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - plan_id
              properties:
                plan_id:
                  type: integer
                  example: 2
                  description: New subscription plan ID (upgrade)
                start_date:
                  type: string
                  format: date-time
                  example: "2026-01-09T17:00:00Z"
                  description: "Optional - New start date (default: today)"
                end_date:
                  type: string
                  format: date-time
                  example: "2026-02-09T17:00:00Z"
                  description: "Optional - New end date (auto-calculated from billing_cycle if not provided)"
      responses:
        200:
          description: Subscription upgraded successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  plan_id:
                    type: integer
                    example: 2
                  household_id:
                    type: integer
                    example: 3
                  start_date:
                    type: string
                    example: "2026-01-09T17:00:00Z"
                  end_date:
                    type: string
                    example: "2026-02-09T17:00:00Z"
                  is_active:
                    type: boolean
                    example: true
        400:
          description: Invalid input or business rule violation
        403:
          description: Forbidden - Subscription does not belong to your household
        404:
          description: Subscription or plan not found
    """
    data = request.get_json()
    
    if not data.get('plan_id'):
        return jsonify({'error': 'plan_id is required'}), 400
    
    # Lấy household_id từ JWT token (tự động từ decorator)
    household_id = get_current_household_id()
    if not household_id:
        return jsonify({'error': 'Household ID is required'}), 400
    
    # Parse start_date và end_date nếu có
    start_date = None
    end_date = None
    if data.get('start_date'):
        start_date = datetime.fromisoformat(data['start_date'].replace("Z", "+00:00")).replace(tzinfo=None)
    if data.get('end_date'):
        end_date = datetime.fromisoformat(data['end_date'].replace("Z", "+00:00")).replace(tzinfo=None)
    
    try:
        # Business rule: Owner tự upgrade subscription của household mình
        # Data isolation: Owner chỉ được update subscription của household mình
        subscription = service.update_own_subscription(
            household_id=household_id,
            plan_id=data['plan_id'],
            start_date=start_date,
            end_date=end_date
        )
        return jsonify(response_schema.dump(subscription)), 200
    except ValueError as e:
        # Business rule violation hoặc not found
        if 'not found' in str(e).lower():
            return jsonify({'error': str(e)}), 404
        if 'does not have an active subscription' in str(e):
            return jsonify({'error': str(e)}), 400
        return jsonify({'error': str(e)}), 400


# ---------------- ADMIN ENDPOINTS (F003: manage_subscriptions) ----------------
# Business Rule: Admin CHỈ được list all subscriptions và deactivate (KHÔNG được create, update plan_id, delete)
@admin_bp.route('', methods=['GET'])
@require_permission(function_code="F003", methods=["GET"])
def list_subscriptions():
    """
    List all subscriptions (Admin only)
    Admin CHỈ được list all subscriptions và deactivate
    ---
    get:
      summary: Get all subscriptions (Admin only - CHỈ list, không create/update plan_id/delete)
      security:
        - Bearer: []
      tags:
        - Admin Subscriptions
      responses:
        200:
          description: List of subscriptions
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
                    plan_id:
                      type: integer
                      example: 2
                    household_id:
                      type: integer
                      example: 3
                    start_date:
                      type: string
                      example: "2026-01-09T17:00:00Z"
                    end_date:
                      type: string
                      example: "2026-02-09T17:00:00Z"
                    is_active:
                      type: boolean
                      example: true
                    created_at:
                      type: string
                      example: "2026-01-09T17:00:00Z"
                    updated_at:
                      type: string
                      example: "2026-01-09T17:00:00Z"
    """
    subs = service.list_subscriptions()
    return jsonify(response_schema.dump(subs, many=True)), 200


@admin_bp.route('/<int:id>', methods=['PUT'])
@require_permission(function_code="F003", methods=["PUT"])
def deactivate_subscription(id):
    """
    Deactivate subscription by ID (Admin only)
    Admin CHỈ được deactivate subscription, KHÔNG được update plan_id, start_date, end_date
    ---
    put:
      summary: Deactivate a subscription (Admin only - CHỈ deactivate, không update plan_id)
      security:
        - Bearer: []
      tags:
        - Admin Subscriptions
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
          description: Subscription ID
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - is_active
              properties:
                is_active:
                  type: boolean
                  example: false
                  description: "CHỈ được set false để deactivate. KHÔNG được set true (Owner tự activate khi upgrade)"
      responses:
        200:
          description: Subscription deactivated successfully
          content:
            application/json:
              schema:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  plan_id:
                    type: integer
                    example: 2
                  household_id:
                    type: integer
                    example: 3
                  start_date:
                    type: string
                    example: "2026-01-09T17:00:00Z"
                  end_date:
                    type: string
                    example: "2026-02-09T17:00:00Z"
                  is_active:
                    type: boolean
                    example: false
        400:
          description: Invalid input - CHỈ được deactivate (is_active=false), không được update plan_id
        403:
          description: Forbidden - KHÔNG được update plan_id, start_date, end_date. CHỈ được deactivate.
        404:
          description: Subscription not found
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Request body is required'}), 400
    
    # Business rule: Admin CHỈ được deactivate subscription (is_active=false)
    # KHÔNG được update plan_id, household_id, start_date, end_date
    if 'plan_id' in data or 'household_id' in data or 'start_date' in data or 'end_date' in data:
        return jsonify({
            'error': 'Admin can only deactivate subscription (is_active=false). '
                    'Cannot update plan_id, household_id, start_date, or end_date. '
                    'Owner must upgrade subscription themselves via PUT /api/owner/subscription'
        }), 403
    
    # CHỈ cho phép update is_active
    if 'is_active' not in data:
        return jsonify({'error': 'is_active field is required. Use false to deactivate.'}), 400
    
    # CHỈ cho phép deactivate (is_active=false), không cho activate (Owner tự activate khi upgrade)
    if data.get('is_active') is True:
        return jsonify({
            'error': 'Admin can only deactivate subscription (is_active=false). '
                    'Cannot activate subscription. Owner must upgrade subscription themselves via PUT /api/owner/subscription'
        }), 403
    
    # Update subscription - CHỈ update is_active
    try:
        sub = service.update_subscription(
            subscription_id=id,
            plan_id=None,  # KHÔNG cho phép update
            household_id=None,  # KHÔNG cho phép update
            start_date=None,  # KHÔNG cho phép update
            end_date=None,  # KHÔNG cho phép update
            is_active=data.get('is_active', False)  # CHỈ update is_active
        )
        return jsonify(response_schema.dump(sub)), 200
    except ValueError as e:
        if 'not found' in str(e).lower():
            return jsonify({'error': str(e)}), 404
        return jsonify({'error': str(e)}), 400
