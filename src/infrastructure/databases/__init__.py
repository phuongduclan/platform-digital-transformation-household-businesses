from infrastructure.databases.mssql import init_mssql, Base

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
    init_mssql(app)