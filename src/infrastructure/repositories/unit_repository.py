from domain.models.unit import Unit
from domain.models.iunit_repository import IUnitRepository
from typing import List, Optional
from infrastructure.models import Unit as UnitModel
from infrastructure.databases.mssql import session

class UnitRepository(IUnitRepository):
    def __init__(self, session=session):
        self.session = session

    def add(self, unit: Unit) -> UnitModel:
        try:
            unit_model = UnitModel(
                household_id=unit.household_id,
                name=unit.name,
                description=unit.description,
                status=unit.status,
                created_at=unit.created_at,
                updated_at=unit.updated_at
            )
            self.session.add(unit_model)
            self.session.commit()
            self.session.refresh(unit_model)
            return unit_model
        except Exception as e:
            self.session.rollback() 
            raise ValueError(f'Error creating unit: {str(e)}')

    def get_by_id(self, unit_id: int, household_id: int) -> Optional[UnitModel]:
        return self.session.query(UnitModel).filter_by(id=unit_id, household_id=household_id).first()

    def list(self, household_id: int) -> List[UnitModel]:
        return self.session.query(UnitModel).filter_by(household_id=household_id).all()
    
    def update(self, unit: Unit) -> UnitModel:
        try:
            unit_model = self.session.query(UnitModel).filter_by(id=unit.id, household_id=unit.household_id).first()
            if not unit_model:
                raise ValueError('Unit not found')
            
            if unit.name is not None:
                unit_model.name = unit.name
            if unit.description is not None:
                unit_model.description = unit.description
            if unit.status is not None:
                unit_model.status = unit.status
            if unit.updated_at is not None:
                unit_model.updated_at = unit.updated_at
            
            self.session.commit()
            self.session.refresh(unit_model)
            return unit_model
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error updating unit: {str(e)}')
        
    def delete(self, unit_id: int, household_id: int) -> None:
        try:
            unit_model = self.session.query(UnitModel).filter_by(id=unit_id, household_id=household_id).first()
            if not unit_model:
                raise ValueError('Unit not found')
            
            self.session.delete(unit_model)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error deleting unit: {str(e)}')