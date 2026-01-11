from domain.models.household import Household
from domain.models.ihousehold_repository import IHouseholdRepository
from typing import List, Optional
from datetime import datetime, timezone
from infrastructure.databases.mssql import session
from infrastructure.models.household_model import Household as HouseholdModel

class HouseholdService:
    def __init__(self, repository: IHouseholdRepository):
        self.repository = repository

    def create_household(
        self,
        tax_code: Optional[str] = None,
        name: Optional[str] = None,
        phone: Optional[str] = None,
        address: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        created_by: Optional[str] = None,
        updated_by: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> Household:
        """
        Create household - Business rules:
        - Validate tax_code unique (nếu có)
        - Default status = "Active" nếu không có
        """
        # Business rule: Validate tax_code unique
        if tax_code:
            existing = session.query(HouseholdModel).filter_by(tax_code=tax_code).first()
            if existing:
                raise ValueError(f"Tax code {tax_code} already exists.")
        
        creator = created_by if created_by is not None else "SYSTEM"
        updater = updated_by if updated_by is not None else "SYSTEM"
        default_status = status if status is not None else "Active"
        
        household = Household(
            id=None,
            tax_code=tax_code,
            name=name,
            phone=phone,
            address=address,
            description=description,
            status=default_status,
            created_by=creator,
            updated_by=updater, 
            created_at=created_at,
            updated_at=updated_at,
        )
        return self.repository.add(household)

    def get_household(self, household_id: int) -> Optional[Household]:
        """Get household by ID - No business rules, use for internal operations"""
        return self.repository.get_by_id(household_id)

    def list_households(self) -> List[Household]:
        """List all households - No business rules, use for internal operations"""
        return self.repository.list()

    def get_own_household(self, household_id: int) -> Optional[Household]:
        """
        Get own household - Business rules:
        - Owner chỉ được lấy household của mình (household_id từ JWT token)
        - KHÔNG được query tất cả households (data isolation)
        - household_id được lấy từ JWT token trong controller, không thể fake được
        - Repository chỉ query theo household_id cụ thể, không query "hết" (all)
        
        Data Isolation: 
        - Owner chỉ xem được household của chính mình (household_id từ JWT)
        - Owner KHÔNG thể query households khác vì household_id được lấy từ JWT token
        - Repository layer chỉ filter theo household_id, không có list all
        """
        # Data isolation: Chỉ query household theo household_id từ JWT
        # Owner không thể query "hết" vì không có endpoint list all households cho Owner
        household = self.repository.get_by_id(household_id)
        if not household:
            raise ValueError(f"Household with ID {household_id} not found.")
        return household

    def update_own_household(
        self,
        household_id: int,
        tax_code: Optional[str] = None,
        name: Optional[str] = None,
        phone: Optional[str] = None,
        address: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        updated_by: Optional[str] = None,
        updated_at: Optional[datetime] = None,
    ) -> Household:
        """
        Update own household - Business rules:
        - Owner chỉ được update household của mình (household_id từ JWT)
        - Validate tax_code unique (nếu thay đổi)
        - Data isolation enforced
        """
        existing_household = self.repository.get_by_id(household_id)
        if not existing_household:
            raise ValueError(f"Household with ID {household_id} not found.")
        
        # Business rule: Validate tax_code unique nếu thay đổi
        if tax_code is not None and tax_code != existing_household.tax_code:
            existing = session.query(HouseholdModel).filter_by(tax_code=tax_code).first()
            if existing:
                raise ValueError(f"Tax code {tax_code} already exists.")
        
        # Update fields
        household_dto = Household(
            id=existing_household.id,
            tax_code=tax_code if tax_code is not None else existing_household.tax_code,
            name=name if name is not None else existing_household.name,
            phone=phone if phone is not None else existing_household.phone,
            address=address if address is not None else existing_household.address,
            description=description if description is not None else existing_household.description,
            status=status if status is not None else existing_household.status,
            created_by=existing_household.created_by,
            updated_by=updated_by if updated_by is not None else existing_household.updated_by,
            created_at=existing_household.created_at,
            updated_at=updated_at if updated_at is not None else datetime.utcnow(),
        )
        return self.repository.update(household_dto)

    def update_household(
        self,
        household_id: int,
        tax_code: Optional[str] = None,
        name: Optional[str] = None,
        phone: Optional[str] = None,
        address: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None,
        created_by: Optional[str] = None,
        updated_by: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> Household:
        """
        Update household - For internal operations (registration flow, etc.)
        Business rules:
        - Validate tax_code unique (nếu thay đổi)
        """
        existing_household = self.repository.get_by_id(household_id)
        if not existing_household:
            raise ValueError(f"Household with ID {household_id} not found.")
        
        # Business rule: Validate tax_code unique nếu thay đổi
        if tax_code is not None and tax_code != existing_household.tax_code:
            existing = session.query(HouseholdModel).filter_by(tax_code=tax_code).first()
            if existing:
                raise ValueError(f"Tax code {tax_code} already exists.")
        
        household_dto = Household(
            id=existing_household.id,
            tax_code=tax_code if tax_code is not None else existing_household.tax_code,
            name=name if name is not None else existing_household.name,
            phone=phone if phone is not None else existing_household.phone,
            address=address if address is not None else existing_household.address,
            description=description if description is not None else existing_household.description,
            status=status if status is not None else existing_household.status,
            created_by=created_by if created_by is not None else existing_household.created_by,
            updated_by=updated_by if updated_by is not None else existing_household.updated_by,
            created_at=created_at if created_at is not None else existing_household.created_at,
            updated_at=updated_at if updated_at is not None else datetime.now(timezone.utc),
        )
        return self.repository.update(household_dto)

    def delete_household(self, household_id: int) -> None:
        """Delete household - For internal operations"""
        self.repository.delete(household_id)