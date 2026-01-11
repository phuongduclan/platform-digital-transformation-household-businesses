"""
Auth Service - Business logic cho authentication
"""
from infrastructure.databases.mssql import session
from infrastructure.models import User as UserModel, Role
from datetime import datetime, timedelta
import jwt
from flask import current_app
from config import Config
from services.subscription_service import SubscriptionService

class AuthService:
    def __init__(self, db_session):
        self.session = db_session
        self.subscription_service = SubscriptionService(db_session)
    
    def authenticate_user(self, user_name: str, password: str):
        """
        Authenticate user với business rules
        
        Returns:
            UserModel nếu thành công
            None nếu không tìm thấy
            Raise ValueError nếu user inactive hoặc subscription không active
        """
        # Query user
        user = self.session.query(UserModel).filter_by(
            user_name=user_name,
            password=password  # So sánh trực tiếp, không hash (theo yêu cầu)
        ).first()
        
        if not user:
            return None
        
        # Business rule: Check user status (case-insensitive)
        if hasattr(user, 'status') and user.status.upper() != 'ACTIVE':
            raise ValueError('User is inactive')
        
        # Business rule: Check subscription cho Owner/Employee (không check cho Admin)
        if user.household_id:  # Owner hoặc Employee (Admin có household_id = NULL)
            # Lấy role để check
            role = self.session.query(Role).filter_by(id=user.role_id).first()
            if role:
                role_name_upper = role.role_name.upper()
                # Chỉ check subscription cho Owner và Employee, không check cho Admin
                # Admin có household_id = NULL nên sẽ không vào đây
                if role_name_upper in ['OWNER', 'EMPLOYEE']:
                    if not self.subscription_service.check_household_subscription_active(user.household_id):
                        raise ValueError('Household subscription is not active. Please contact administrator.')
        
        return user
    
    def generate_jwt_token(self, user):
        """
        Generate JWT token với đầy đủ thông tin (theo cam kết)
        
        Args:
            user: UserModel object
            
        Returns:
            str: JWT token
        """
        payload = {
            'user_id': user.id,
            'role_id': user.role_id,
            'household_id': user.household_id,  # None nếu Admin
            'exp': datetime.utcnow() + timedelta(hours=24)
        }
        
        # Lấy SECRET_KEY từ current_app hoặc Config
        try:
            secret_key = current_app.config['SECRET_KEY']
        except RuntimeError:
            # Không có app context, dùng Config
            secret_key = Config.SECRET_KEY
        
        token = jwt.encode(payload, secret_key, algorithm='HS256')
        return token
    
    def get_user_by_id(self, user_id: int):
        """
        Get user by id
        
        Returns:
            UserModel hoặc None
        """
        return self.session.query(UserModel).filter_by(id=user_id).first()
    
    def decode_token(self, token: str):
        """
        Decode JWT token
        
        Returns:
            dict: Payload
            Raise ValueError nếu token invalid/expired
        """
        # Lấy SECRET_KEY từ current_app hoặc Config
        try:
            secret_key = current_app.config['SECRET_KEY']
        except RuntimeError:
            # Không có app context, dùng Config
            secret_key = Config.SECRET_KEY
        
        try:
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError('Token expired')
        except jwt.InvalidTokenError:
            raise ValueError('Invalid token')
