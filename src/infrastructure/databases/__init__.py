# Use PostgreSQL for Supabase deployment
from infrastructure.databases.postgres import init_postgres, Base as PostgresBase, session as postgres_session, engine as postgres_engine

# Re-export for backward compatibility - all files importing from infrastructure.databases.mssql will get PostgreSQL connection
Base = PostgresBase
session = postgres_session
engine = postgres_engine

# Migration Entities -> Tables
def init_db(app):
    # Import models here to avoid circular import
    from infrastructure.models import (
        AccountingLedger,
        Category,
        Customer,
        DebtRecord,
        ExportDetail,
        ExportReceipt,
        Function,
        Household,
        ImportDetail,
        ImportReceipt,
        Inventory,
        InvoiceDetail,
        Invoice,
        Payment,
        PaymentMethod,
        Product,
        Role,
        RoleFunction,
        Seller,
        Subscription,
        SubscriptionPlan,
        TodoModel,
        Unit,
        User,
        Warehouse
    )
    init_postgres(app)

# Re-export session and Base so files can import from __init__.py or mssql.py
__all__ = ['init_db', 'Base', 'session', 'engine']