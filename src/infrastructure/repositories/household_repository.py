from domain.models.ihousehold_repository import IHouseholdRepository
from domain.models.household import Household
from typing import List, Optional
from infrastructure.models.household_model import Household as HouseholdModel
from infrastructure.databases.mssql import session
from sqlalchemy.orm import Session
from datetime import datetime, timezone

class HouseholdRepository(IHouseholdRepository):
    def __init__(self, session: Session = session):
        self.session = session

    def add(self, household: Household) -> HouseholdModel:
        """
        Add household to session (NO COMMIT - let controller manage transaction)
        Transaction management: Controller phải commit/rollback
        """
        try:
            household_model = HouseholdModel(
                tax_code=household.tax_code,
                name=household.name,
                phone=household.phone,
                address=household.address,
                description=household.description,
                status=household.status or 'Active',
                created_by=household.created_by or "SYSTEM",
                updated_by=household.updated_by or "SYSTEM", 
                created_at=(household.created_at.replace(tzinfo=None) if household.created_at and household.created_at.tzinfo else household.created_at) if household.created_at else datetime.now(timezone.utc).replace(tzinfo=None),
                updated_at=(household.updated_at.replace(tzinfo=None) if household.updated_at and household.updated_at.tzinfo else household.updated_at) if household.updated_at else datetime.now(timezone.utc).replace(tzinfo=None)
            )
            self.session.add(household_model)
            # KHÔNG commit ở đây - để controller quản lý transaction
            # self.session.commit()
            self.session.flush()  # Flush để lấy ID, nhưng không commit
            return household_model
        except Exception as e:
            # KHÔNG rollback ở đây - để controller quản lý transaction
            # self.session.rollback()
            raise ValueError(f'Error creating household: {str(e)}')

    def get_by_id(self, household_id: int) -> Optional[HouseholdModel]:
        """Get household by ID (NO session.close - let controller manage session)"""
        return self.session.query(HouseholdModel).filter_by(id=household_id).first()

    def list(self) -> List[HouseholdModel]:
        """List all households (NO session.close - let controller manage session)"""
        return self.session.query(HouseholdModel).all()

    def update(self, household: Household) -> HouseholdModel:
        try:
            household_model = self.session.query(HouseholdModel).filter_by(id=household.id).first()
            if not household_model:
                raise ValueError('Household not found')

            # Update tất cả fields từ DTO
            if household.tax_code is not None:
                household_model.tax_code = household.tax_code
            if household.name is not None:
                household_model.name = household.name
            if household.phone is not None:
                household_model.phone = household.phone
            if household.address is not None:
                household_model.address = household.address
            if household.description is not None:
                household_model.description = household.description
            if household.status is not None:
                household_model.status = household.status
            if household.updated_by is not None:
                household_model.updated_by = household.updated_by
            # Remove timezone if present (SQL Server không support timezone-aware datetime)
            updated_at_value = household.updated_at
            if updated_at_value and hasattr(updated_at_value, 'tzinfo') and updated_at_value.tzinfo:
                updated_at_value = updated_at_value.replace(tzinfo=None)
            household_model.updated_at = updated_at_value or datetime.utcnow()

            # KHÔNG commit ở đây - để controller quản lý transaction
            # self.session.commit()
            self.session.flush()  # Flush để refresh, nhưng không commit
            return household_model
        except Exception as e:
            # KHÔNG rollback ở đây - để controller quản lý transaction
            # self.session.rollback()
            raise ValueError(f'Error updating household: {str(e)}')

    def delete(self, household_id: int) -> None:
        """
        Delete household from session (NO COMMIT - let controller manage transaction)
        """
        household_model = self.session.query(HouseholdModel).filter_by(id=household_id).first()
        if household_model:
            self.session.delete(household_model)
            # KHÔNG commit ở đây - để controller quản lý transaction
            # self.session.commit()
        else:
            raise ValueError('Household not found')
