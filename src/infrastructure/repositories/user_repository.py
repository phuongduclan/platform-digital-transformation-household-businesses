from domain.models.iuser_repository import IUserRepository
from domain.models.user import User
from typing import List, Optional
from infrastructure.models.user_model import UserModel
from infrastructure.databases.mssql import session

class UserRepository(IUserRepository):
    def __init__(self, session=session):
        self.session = session

    def add(self, user: User) -> UserModel:
        try:
            user_model = UserModel(
                household_id=user.household_id,
                role_id=user.role_id,
                username=user.username, # Renamed from user_name
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
            self.session.commit()
            self.session.refresh(user_model)
            return user_model
        except Exception as e:
            self.session.rollback()
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
            if user.username is not None:
                user_model.username = user.username
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
