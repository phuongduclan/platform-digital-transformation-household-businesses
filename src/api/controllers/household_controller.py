from flask import Blueprint, request, jsonify
from services.household_service import HouseholdService
from infrastructure.repositories.household_repository import HouseholdRepository
from api.schemas.household import HouseholdRequestSchema, HouseholdResponseSchema
from api.decorators.auth_decorators import require_permission
from api.utils.auth_utils import get_current_household_id
from infrastructure.databases.mssql import session
from datetime import datetime, timezone

# Owner endpoints only - Admin không có quyền quản lý Household
owner_bp = Blueprint('owner_household', __name__, url_prefix='/api/owner/household')

household_service = HouseholdService(HouseholdRepository(session=session))
request_schema = HouseholdRequestSchema()
response_schema = HouseholdResponseSchema()


# ---------------- Owner Routes (F102: view_own_household - R, U) ----------------
@owner_bp.route('', methods=['GET'])
@require_permission(function_code="F102", methods=["GET"])
def get_own_household():
    """
    Get own household (Owner only)
    ---
    get:
      summary: Get the household of the current owner
      security:
        - Bearer: []
      tags:
        - Owner Household
      responses:
        200:
          description: Household object
          content:
            application/json:
              schema:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  tax_code:
                    type: string
                    example: "123456789012"
                  name:
                    type: string
                    example: "Owner Household"
                  phone:
                    type: string
                    example: "0901234567"
                  address:
                    type: string
                    example: "789 Owner St"
                  description:
                    type: string
                    example: "Household description"
                  status:
                    type: string
                    example: "Active"
                  created_at:
                    type: string
                    example: "2026-01-09T17:00:00Z"
                  updated_at:
                    type: string
                    example: "2026-01-09T18:00:00Z"
        400:
          description: Household ID is required
        403:
          description: Forbidden - Household does not belong to you
        404:
          description: Household not found
    """
    # Lấy household_id từ JWT token (tự động từ decorator)
    # Data isolation: household_id được lấy từ JWT token, Owner không thể fake được
    household_id = get_current_household_id()
    if not household_id:
        return jsonify({'error': 'Household ID is required'}), 400
    
    try:
        # Data isolation: Owner chỉ lấy household của mình
        # Business rule: Owner KHÔNG được query "hết" (tất cả households)
        # Chỉ query household theo household_id từ JWT token
        household = household_service.get_own_household(household_id)
        if not household:
            return jsonify({'message': 'Household not found'}), 404
        return jsonify(response_schema.dump(household)), 200
    except ValueError as e:
        if 'not found' in str(e).lower():
            return jsonify({'error': str(e)}), 404
        return jsonify({'error': str(e)}), 403


@owner_bp.route('', methods=['PUT'])
@require_permission(function_code="F102", methods=["PUT"])
def update_own_household():
    """
    Update own household (Owner only)
    ---
    put:
      summary: Update the household of the current owner
      security:
        - Bearer: []
      tags:
        - Owner Household
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              properties:
                tax_code:
                  type: string
                  example: "123456789012"
                name:
                  type: string
                  example: "Owner Household Updated"
                phone:
                  type: string
                  example: "0901234567"
                address:
                  type: string
                  example: "987 Owner St"
                description:
                  type: string
                  example: "Updated description"
                status:
                  type: string
                  example: "Active"
      responses:
        200:
          description: Updated household
          content:
            application/json:
              schema:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  tax_code:
                    type: string
                    example: "123456789012"
                  name:
                    type: string
                    example: "Owner Household Updated"
                  phone:
                    type: string
                    example: "0901234567"
                  address:
                    type: string
                    example: "987 Owner St"
                  description:
                    type: string
                    example: "Updated description"
                  status:
                    type: string
                    example: "Active"
                  created_at:
                    type: string
                    example: "2026-01-09T17:00:00Z"
                  updated_at:
                    type: string
                    example: "2026-01-09T18:00:00Z"
        400:
          description: Invalid input
        403:
          description: Forbidden - Household does not belong to you
        404:
          description: Household not found
    """
    data = request.get_json()
    errors = request_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    # Lấy household_id từ JWT token (tự động từ decorator)
    household_id = get_current_household_id()
    if not household_id:
        return jsonify({'error': 'Household ID is required'}), 400
    
    try:
        # Data isolation: Owner chỉ update household của mình
        # Business rules được xử lý ở Application Layer (HouseholdService)
        household = household_service.update_own_household(
            household_id=household_id,
            tax_code=data.get('tax_code'),
            name=data.get('name'),
            phone=data.get('phone'),
            address=data.get('address'),
            description=data.get('description'),
            status=data.get('status'),
            updated_by=data.get('updated_by'),
            updated_at=datetime.now(timezone.utc)
        )
        return jsonify(response_schema.dump(household)), 200
    except ValueError as e:
        # Business rule violation hoặc household not found từ service
        if 'not found' in str(e).lower():
            return jsonify({'error': str(e)}), 404
        if 'belong' in str(e).lower() or 'forbidden' in str(e).lower():
            return jsonify({'error': str(e)}), 403
        return jsonify({'error': str(e)}), 400
