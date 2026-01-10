from sqlalchemy import Column, ForeignKey, Integer
from infrastructure.databases.base import Base

class ImportDetail(Base):
    __tablename__ = 'import_details'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    import_id = Column(Integer, ForeignKey("import_receipts.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    unit_id = Column(Integer, ForeignKey("units.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
