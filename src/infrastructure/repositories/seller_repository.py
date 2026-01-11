from domain.models.iseller_repository import ISellerRepository
from domain.models.seller import Seller
from typing import List, Optional
from infrastructure.models.seller_model import Seller as SellerModel
from infrastructure.databases.mssql import session

class SellerRepository(ISellerRepository):
    def __init__(self, session=session):
        self.session = session

    def create(self, seller: Seller) -> Seller:
        try:
            seller_model = SellerModel(
                household_id=seller.household_id,
                tax_code=seller.tax_code,
                name=seller.name,
                phone=seller.phone,
                address=seller.address,
                description=seller.description,
                status=seller.status,
                created_by=seller.created_by,
                updated_by=seller.updated_by,
                created_at=seller.created_at,
                updated_at=seller.updated_at
            )
            self.session.add(seller_model)
            self.session.commit()
            self.session.refresh(seller_model)
            return self._to_domain(seller_model)
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error creating seller: {str(e)}')

    def get_by_id(self, seller_id: int, household_id: int = None) -> Optional[Seller]:
        query = self.session.query(SellerModel).filter_by(id=seller_id)
        if household_id is not None:
            query = query.filter_by(household_id=household_id)
        seller_model = query.first()
        return self._to_domain(seller_model) if seller_model else None

    def list(self, household_id: int, status: str = None) -> List[Seller]:
        query = self.session.query(SellerModel).filter_by(household_id=household_id)
        if status is not None:
            query = query.filter_by(status=status)
        seller_models = query.all()
        return [self._to_domain(sm) for sm in seller_models]

    def update(self, seller: Seller) -> Seller:
        try:
            seller_model = self.session.query(SellerModel).filter_by(
                id=seller.id,
                household_id=seller.household_id
            ).first()
            if not seller_model:
                raise ValueError('Seller not found')

            if seller.tax_code is not None:
                seller_model.tax_code = seller.tax_code
            if seller.name is not None:
                seller_model.name = seller.name
            if seller.phone is not None:
                seller_model.phone = seller.phone
            if seller.address is not None:
                seller_model.address = seller.address
            if seller.description is not None:
                seller_model.description = seller.description
            if seller.status is not None:
                seller_model.status = seller.status
            if seller.updated_by is not None:
                seller_model.updated_by = seller.updated_by
            if seller.updated_at is not None:
                seller_model.updated_at = seller.updated_at

            self.session.commit()
            self.session.refresh(seller_model)
            return self._to_domain(seller_model)
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error updating seller: {str(e)}')

    def delete(self, seller_id: int, household_id: int = None) -> None:
        try:
            query = self.session.query(SellerModel).filter_by(id=seller_id)
            if household_id is not None:
                query = query.filter_by(household_id=household_id)
            seller_model = query.first()
            if seller_model:
                self.session.delete(seller_model)
                self.session.commit()
            else:
                raise ValueError('Seller not found')
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error deleting seller: {str(e)}')

    def _to_domain(self, seller_model: SellerModel) -> Seller:
        return Seller(
            id=seller_model.id,
            household_id=seller_model.household_id,
            tax_code=seller_model.tax_code,
            name=seller_model.name,
            phone=seller_model.phone,
            address=seller_model.address,
            description=seller_model.description,
            status=seller_model.status,
            created_by=seller_model.created_by,
            updated_by=seller_model.updated_by,
            created_at=seller_model.created_at,
            updated_at=seller_model.updated_at
        )
