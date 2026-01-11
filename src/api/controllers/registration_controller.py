from flask import Blueprint, request, jsonify
from services.household_service import HouseholdService
from services.user_service import UserService
from services.subscription_service import SubscriptionService
from services.subscription_plan_service import SubscriptionPlanService
from infrastructure.repositories.household_repository import HouseholdRepository
from infrastructure.repositories.user_repository import UserRepository
from infrastructure.repositories.subscription_plan_repository import SubscriptionPlanRepository
from infrastructure.databases.mssql import session
from infrastructure.models import Role
from datetime import datetime, timezone, timedelta
bp = Blueprint('public_registration', __name__, url_prefix='/api/public')

household_service = HouseholdService(HouseholdRepository(session=session))
user_service = UserService(UserRepository(session=session))
subscription_service = SubscriptionService(session)
subscription_plan_service = SubscriptionPlanService(SubscriptionPlanRepository(session=session))


@bp.route('/register', methods=['POST'])
def register_owner():
    """
    Owner Registration Flow (Public - No auth required)
    Flow: Tạo Household → Tạo Owner Account → Tạo Subscription
    
    ---
    post:
      summary: Register new Owner account with Household and Subscription
      tags:
        - Public Registration
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - plan_id
                - household
                - owner_account
              properties:
                plan_id:
                  type: integer
                  example: 1
                  description: Subscription Plan ID (chọn từ GET /api/public/subscription-plans)
                household:
                  type: object
                  required:
                    - name
                  properties:
                    tax_code:
                      type: string
                      example: "123456789012"
                    name:
                      type: string
                      example: "Household Name"
                    phone:
                      type: string
                      example: "0901234567"
                    address:
                      type: string
                      example: "123 Main St"
                    description:
                      type: string
                      example: "Household description"
                owner_account:
                  type: object
                  required:
                    - user_name
                    - password
                  properties:
                    user_name:
                      type: string
                      example: "owner1"
                    password:
                      type: string
                      example: "password123"
                    email:
                      type: string
                      example: "owner@example.com"
                    description:
                      type: string
                      example: "Owner account description"
      responses:
        201:
          description: Registration successful
          content:
            application/json:
              schema:
                type: object
                properties:
                  message:
                    type: string
                    example: "Registration successful"
                  household_id:
                    type: integer
                    example: 1
                  user_id:
                    type: integer
                    example: 1
                  subscription_id:
                    type: integer
                    example: 1
        400:
          description: Invalid input or business rule violation
        404:
          description: Subscription plan not found
    """
    data = request.get_json()
    
    # Validate required fields
    if not data.get('plan_id'):
        return jsonify({'error': 'plan_id is required'}), 400
    if not data.get('household'):
        return jsonify({'error': 'household is required'}), 400
    if not data.get('owner_account'):
        return jsonify({'error': 'owner_account is required'}), 400
    
    household_data = data['household']
    owner_account_data = data['owner_account']
    plan_id = data['plan_id']
    
    # Validate household required fields
    if not household_data.get('name'):
        return jsonify({'error': 'household.name is required'}), 400
    
    # Validate owner account required fields
    if not owner_account_data.get('user_name'):
        return jsonify({'error': 'owner_account.user_name is required'}), 400
    if not owner_account_data.get('password'):
        return jsonify({'error': 'owner_account.password is required'}), 400
    
    # Transaction: Tạo Household → Owner User → Subscription (All-or-Nothing)
    # Business Rule: Subscription tự động tạo khi Owner đăng ký (không cần ai tạo thủ công)
    # Tất cả các bước phải thành công, nếu không thì rollback hết
    # Begin transaction - tất cả operations trong cùng 1 transaction
    try:
        # Bước 1: Validate subscription plan tồn tại và active (read-only, không cần transaction)
        plan = subscription_plan_service.get_plan(plan_id)
        if not plan:
            return jsonify({'error': f'Subscription plan with ID {plan_id} not found'}), 404
        
        plan_obj = plan  # Get actual model if needed
        if hasattr(plan, 'status') and getattr(plan, 'status', '').lower() != 'active':
            return jsonify({'error': f'Subscription plan with ID {plan_id} is not active'}), 400
        
        # Bước 2: Lấy Owner role (trong cùng session với transaction)
        # Query Owner role trong cùng session để tránh "not bound to Session" error
        owner_role = session.query(Role).filter_by(role_name='Owner').first()
        if not owner_role:
            # Try case-insensitive
            all_roles = session.query(Role).all()
            owner_role = next((r for r in all_roles if r.role_name.upper() == 'OWNER'), None)
            if not owner_role:
                return jsonify({'error': 'Owner role not found in database'}), 500
        
        # Lấy role_id ngay lập tức (trước khi có bất kỳ operation nào khác) để tránh "not bound to Session"
        owner_role_id = owner_role.id
        
        # Bước 3: Tạo Household (chưa commit - sẽ commit cùng lúc với User và Subscription)
        now = datetime.now(timezone.utc)
        household = household_service.create_household(
            tax_code=household_data.get('tax_code'),
            name=household_data.get('name'),
            phone=household_data.get('phone'),
            address=household_data.get('address'),
            description=household_data.get('description'),
            status='Active',
            created_by='REGISTRATION',
            updated_by='REGISTRATION',
            created_at=now,
            updated_at=now
        )
        household_id = household.id if hasattr(household, 'id') else household
        
        # Bước 4: Tạo Owner User account (chưa commit - sẽ commit cùng lúc với Household và Subscription)
        # Password không hash (theo yêu cầu - auth_service so sánh trực tiếp)
        # Dùng owner_role_id (đã lấy trước đó) thay vì owner_role.id để tránh "not bound to Session"
        owner_user = user_service.create_user(
            household_id=household_id,
            role_id=owner_role_id,  # Dùng ID đã lấy trước đó
            user_name=owner_account_data['user_name'],
            password=owner_account_data['password'],
            email=owner_account_data.get('email'),
            description=owner_account_data.get('description'),
            status='Active',
            created_by='REGISTRATION',
            is_admin_creating=False  # Public registration, không phải Admin
        )
        user_id = owner_user.id if hasattr(owner_user, 'id') else owner_user
        
        # Bước 5: Tạo Subscription (tự động - business rule)
        # Tính end_date dựa trên billing_cycle (nếu có) hoặc default 1 tháng
        billing_cycle = getattr(plan_obj, 'billing_cycle', 'monthly') if hasattr(plan_obj, 'billing_cycle') else 'monthly'
        
        start_date = now.replace(tzinfo=None) if now.tzinfo else now  # Remove timezone for SQL Server
        if billing_cycle.lower() == 'monthly':
            end_date = start_date + timedelta(days=30)
        elif billing_cycle.lower() == 'yearly':
            end_date = start_date + timedelta(days=365)
        else:
            # Default: 30 days
            end_date = start_date + timedelta(days=30)
        
        # Business rule: Registration flow - subscription tự động tạo
        # allow_multiple=True để bypass business rule check (vì đây là household mới)
        subscription = subscription_service.create_subscription(
            household_id=household_id,
            plan_id=plan_id,
            start_date=start_date,
            end_date=end_date,
            is_active=True,
            allow_multiple=True  # Registration flow: household mới, không có subscription cũ
        )
        subscription_id = subscription.id if hasattr(subscription, 'id') else subscription
        
        # Commit transaction - Tất cả 3 bước (Household, User, Subscription) commit cùng lúc
        # Tất cả repositories đã flush (không commit), bây giờ commit một lần duy nhất
        session.commit()
        
        return jsonify({
            'message': 'Registration successful',
            'household_id': household_id,
            'user_id': user_id,
            'subscription_id': subscription_id
        }), 201
        
    except ValueError as e:
        session.rollback()
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        session.rollback()
        return jsonify({'error': f'Registration failed: {str(e)}'}), 500
