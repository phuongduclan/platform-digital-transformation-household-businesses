from domain.models.unit import Unit
from domain.models.iunit_repository import IUnitRepository
from typing import List, Optional
from datetime import datetime

class UnitService:
    def __init__(self, repository: IUnitRepository):
        self.repository = repository

    def create_unit(self, household_id: int, name: str, description: str = None, status: str = None) -> Unit:
        now = datetime.utcnow()
        unit = Unit(id=None, household_id=household_id, name=name, description=description,
                   status=status, created_at=now, updated_at=now)
        return self.repository.add(unit)

    def get_unit(self, unit_id: int, household_id: int) -> Optional[Unit]:
        return self.repository.get_by_id(unit_id, household_id)

    def list_units(self, household_id: int) -> List[Unit]:
        return self.repository.list(household_id)

    def update_unit(self, unit_id: int, household_id: int, name: str = None, description: str = None, status: str = None) -> Unit:
        now = datetime.utcnow()
        unit = Unit(id=unit_id, household_id=household_id, name=name, description=description, status=status, updated_at=now)
        return self.repository.update(unit)

    def delete_unit(self, unit_id: int, household_id: int) -> None:
        self.repository.delete(unit_id, household_id)