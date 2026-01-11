from domain.models.iuser_repository import IUserRepository
from domain.models.user import User
from typing import List, Optional
from infrastructure.models import User as UserModel
from infrastructure.databases.mssql import session
from sqlalchemy import func, or_

class UserRepository(IUserRepository):
    def __init__(self, session=session):
        self.session = session

    def add(self, user: User) -> UserModel:
        """
        Add user to session (NO COMMIT - let controller manage transaction)
        Transaction management: Controller phải commit/rollback
        """
        try:
            user_model = UserModel(
                household_id=user.household_id,
                role_id=user.role_id,
                user_name=user.user_name,
                password=user.password,
                email=user.email,
                description=user.description,
                status=user.status,
                created_by=user.created_by,
                updated_by=user.updated_by,
                created_at=user.created_at,
                updated_at=user.updated_at
            )
            self.session.add(user_model)
            # KHÔNG commit ở đây - để controller quản lý transaction
            # self.session.commit()
            self.session.flush()  # Flush để lấy ID, nhưng không commit
            return user_model
        except Exception as e:
            # KHÔNG rollback ở đây - để controller quản lý transaction
            # self.session.rollback()
            raise ValueError(f'Error creating user: {str(e)}')

    def get_by_id(self, user_id: int) -> Optional[UserModel]:
        return self.session.query(UserModel).filter_by(id=user_id).first()

    def list(self) -> List[UserModel]:
        return self.session.query(UserModel).all()

    def update(self, user: User) -> UserModel:
        try:
            user_model = self.session.query(UserModel).filter_by(id=user.id).first()
            if not user_model:
                raise ValueError('User not found')
            
            if user.household_id is not None:
                user_model.household_id = user.household_id
            if user.role_id is not None:
                user_model.role_id = user.role_id
            if user.user_name is not None:
                user_model.user_name = user.user_name
            if user.password is not None:
                user_model.password = user.password
            if user.email is not None:
                user_model.email = user.email
            if user.description is not None:
                user_model.description = user.description
            if user.status is not None:
                user_model.status = user.status
            if user.updated_by is not None:
                user_model.updated_by = user.updated_by
            if user.updated_at is not None:
                user_model.updated_at = user.updated_at
            
            self.session.commit()
            self.session.refresh(user_model)
            return user_model
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error updating user: {str(e)}')

    def delete(self, user_id: int) -> None:
        try:
            user = self.session.query(UserModel).filter_by(id=user_id).first()
            if user:
                self.session.delete(user)
                self.session.commit()
            else:
                raise ValueError('User not found')
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error deleting user: {str(e)}')

    def get_by_household_id(self, household_id: int) -> List[UserModel]:
        return self.session.query(UserModel).filter_by(household_id=household_id).all()
    
    def list_exclude_role(self, exclude_role_id: int) -> List[UserModel]:
        """List all users except users with specific role_id"""
        return self.session.query(UserModel).filter(UserModel.role_id != exclude_role_id).all()
    
    def search_and_filter(self, exclude_role_id: int = None, role_id: int = None, 
                         status: str = None, household_id: int = None,
                         search_term: str = None) -> List[UserModel]:
        """
        Search and filter users
        
        Business Logic: Admin quản lý Owner accounts - view, search, filter, manage
        
        Args:
            exclude_role_id: Exclude users with this role_id (e.g., exclude Employee for Admin)
            role_id: Filter by role_id (e.g., only Owner role)
            status: Filter by status (Active, Inactive) - để activate/deactivate
            household_id: Filter by household_id
            search_term: Search by user_name or email (case-insensitive, partial match) - để search Owner accounts
        """
        query = self.session.query(UserModel)
        
        # Filter: Exclude role (Admin exclude Employee)
        if exclude_role_id is not None:
            query = query.filter(UserModel.role_id != exclude_role_id)
        
        # Filter: By role_id (e.g., only Owner)
        if role_id is not None:
            query = query.filter(UserModel.role_id == role_id)
        
        # Filter: By status (Active, Inactive) - để activate/deactivate Owner accounts
        if status is not None:
            query = query.filter(UserModel.status == status)
        
        # Filter: By household_id
        if household_id is not None:
            query = query.filter(UserModel.household_id == household_id)
        
        # Search: By user_name or email (case-insensitive, partial match)
        if search_term:
            search_pattern = f'%{search_term}%'
            query = query.filter(
                (UserModel.user_name.ilike(search_pattern)) | 
                (UserModel.email.ilike(search_pattern))
            )
        
        return query.all()