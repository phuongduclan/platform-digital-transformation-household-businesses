from domain.models.icustomer_repository import ICustomerRepository
from domain.models.customer import Customer
from typing import List, Optional
from infrastructure.models.customer_model import Customer as CustomerModel
from infrastructure.databases.mssql import session

class CustomerRepository(ICustomerRepository):
    def __init__(self, session=session):
        self.session = session

    def create(self, customer: Customer) -> Customer:
        try:
            customer_model = CustomerModel(
                household_id=customer.household_id,
                tax_code=customer.tax_code,
                name=customer.name,
                phone=customer.phone,
                address=customer.address,
                description=customer.description,
                status=customer.status,
                created_by=customer.created_by,
                updated_by=customer.updated_by,
                created_at=customer.created_at,
                updated_at=customer.updated_at
            )
            self.session.add(customer_model)
            self.session.commit()
            self.session.refresh(customer_model)
            return self._to_domain(customer_model)
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error creating customer: {str(e)}')

    def get_by_id(self, customer_id: int, household_id: int = None) -> Optional[Customer]:
        query = self.session.query(CustomerModel).filter_by(id=customer_id)
        if household_id is not None:
            query = query.filter_by(household_id=household_id)
        customer_model = query.first()
        return self._to_domain(customer_model) if customer_model else None

    def list(self, household_id: int, status: str = None) -> List[Customer]:
        query = self.session.query(CustomerModel).filter_by(household_id=household_id)
        if status is not None:
            query = query.filter_by(status=status)
        customer_models = query.all()
        return [self._to_domain(cm) for cm in customer_models]

    def update(self, customer: Customer) -> Customer:
        try:
            customer_model = self.session.query(CustomerModel).filter_by(
                id=customer.id,
                household_id=customer.household_id
            ).first()
            if not customer_model:
                raise ValueError('Customer not found')

            if customer.tax_code is not None:
                customer_model.tax_code = customer.tax_code
            if customer.name is not None:
                customer_model.name = customer.name
            if customer.phone is not None:
                customer_model.phone = customer.phone
            if customer.address is not None:
                customer_model.address = customer.address
            if customer.description is not None:
                customer_model.description = customer.description
            if customer.status is not None:
                customer_model.status = customer.status
            if customer.updated_by is not None:
                customer_model.updated_by = customer.updated_by
            if customer.updated_at is not None:
                customer_model.updated_at = customer.updated_at

            self.session.commit()
            self.session.refresh(customer_model)
            return self._to_domain(customer_model)
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error updating customer: {str(e)}')

    def delete(self, customer_id: int, household_id: int = None) -> None:
        try:
            query = self.session.query(CustomerModel).filter_by(id=customer_id)
            if household_id is not None:
                query = query.filter_by(household_id=household_id)
            customer_model = query.first()
            if customer_model:
                self.session.delete(customer_model)
                self.session.commit()
            else:
                raise ValueError('Customer not found')
        except Exception as e:
            self.session.rollback()
            raise ValueError(f'Error deleting customer: {str(e)}')

    def _to_domain(self, customer_model: CustomerModel) -> Customer:
        return Customer(
            id=customer_model.id,
            household_id=customer_model.household_id,
            tax_code=customer_model.tax_code,
            name=customer_model.name,
            phone=customer_model.phone,
            address=customer_model.address,
            description=customer_model.description,
            status=customer_model.status,
            created_by=customer_model.created_by,
            updated_by=customer_model.updated_by,
            created_at=customer_model.created_at,
            updated_at=customer_model.updated_at
        )
