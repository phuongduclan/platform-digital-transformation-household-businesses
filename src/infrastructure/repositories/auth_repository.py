from domain.models.iauth_repository import IAuthRepository
from domain.models.user import User
from typing import List, Optional
from sqlalchemy.orm import Session
from infrastructure.models.user_model import UserModel
from infrastructure.databases.mssql import session

class AuthRepository(IAuthRepository):
    def __init__(self, session: Session = session):
        self.session = session
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        user_model = self.session.query(UserModel).filter_by(username=username).first()
        if not user_model:
            return None
        # Map UserModel to Domain User
        return User(
            id=user_model.id,
            username=user_model.username,
            password=user_model.password,
            email=user_model.email,
            household_id=user_model.household_id,
            role_id=user_model.role_id,
            status=user_model.status,
            description=user_model.description,
            created_by=user_model.created_by,
            updated_by=user_model.updated_by,
            created_at=user_model.created_at,
            updated_at=user_model.updated_at
        )

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        user_model = self.session.query(UserModel).filter_by(id=user_id).first()
        if not user_model:
            return None
        return User(
            id=user_model.id,
            username=user_model.username,
            password=user_model.password,
            email=user_model.email,
            household_id=user_model.household_id,
            role_id=user_model.role_id,
            status=user_model.status,
            description=user_model.description,
            created_by=user_model.created_by,
            updated_by=user_model.updated_by,
            created_at=user_model.created_at,
            updated_at=user_model.updated_at
        )

    def register(self, user: User) -> Optional[User]:
        try:
            new_user = UserModel(
                username=user.username,
                password=user.password,
                email=user.email,
                role_id=user.role_id if user.role_id else 2, # Default to Employee if not set? Or check logic.
                household_id=user.household_id,
                status=user.status or 'ACTIVE'
            )
            self.session.add(new_user)
            self.session.commit()
            self.session.refresh(new_user)
            user.id = new_user.id
            return user
        except Exception as e:
            self.session.rollback()
            raise e # Let Service handle or return None?
        
    def remember_password(self) -> Optional[User]:
        return None
        
    def look_account(self, Id: int) -> bool:
        return True
        
    def un_look_account(self, course_id: int) -> None:
        pass
        
    def check_exist(self, username: str) -> bool:
        existing_user = self.session.query(UserModel).filter_by(username=username).first()
        return True if existing_user else False
