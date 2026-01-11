# CÂY THƯ MỤC SCREEN FLOW THEO ROLE

Dựa trên Documents.md và 25 Models trong infrastructure/models/

---

## 🔐 AUTH FLOW (Dùng chung cho tất cả Roles)

### Login & Logout
```
screens/
├── auth/
│   ├── LoginScreen.tsx                        # Login chung cho Admin/Owner/Employee
│   │                                         # - Username/Password input
│   │                                         # - Auto detect role sau khi login
│   │                                         # - Redirect theo role:
│   │                                         #   + Admin → AdminDashboardScreen
│   │                                         #   + Owner → OwnerDashboardScreen
│   │                                         #   + Employee → EmployeeHomeScreen
│   │
│   ├── LogoutScreen.tsx                       # Logout chung
│   │                                         # - Clear session/token
│   │                                         # - Redirect về LoginScreen
│   │
│   └── ForgotPasswordScreen.tsx              # Quên mật khẩu (optional)
```

### Registration Flow (Chỉ cho Owner - Public, không cần auth)
```
screens/
├── registration/
│   ├── SubscriptionPlanSelectionScreen.tsx    # Bước 1: Chọn gói đăng ký
│   │                                         # - GET /api/public/subscription-plans (Public endpoint)
│   │                                         # - Hiển thị danh sách subscription plans (active only)
│   │                                         # - So sánh các gói (Basic, Pro, etc.)
│   │                                         # - Chọn gói đăng ký (lưu plan_id)
│   │
│   ├── HouseholdRegistrationScreen.tsx       # Bước 2: Điền thông tin hộ kinh doanh
│   │                                         # - Tên hộ kinh doanh (name) - required
│   │                                         # - Mã số thuế (tax_code) - CCCD người đại diện (optional, unique)
│   │                                         # - Số điện thoại (phone) - optional
│   │                                         # - Địa chỉ (address) - optional
│   │                                         # - Mô tả (description) - optional
│   │                                         # - Status: Active (auto-assign)
│   │
│   ├── OwnerAccountCreationScreen.tsx        # Bước 3: Tạo tài khoản Owner
│   │                                         # - Username (user_name) - required, unique
│   │                                         # - Password (password) - required
│   │                                         # - Confirm Password
│   │                                         # - Email (optional)
│   │                                         # - Description (optional)
│   │                                         # - POST /api/public/register (Public endpoint)
│   │                                         #   Tạo tất cả trong 1 transaction:
│   │                                         #   + Tạo Household (từ bước 2)
│   │                                         #   + Tạo Owner User account (role Owner, link với household)
│   │                                         #   + Tạo Subscription (với plan_id từ bước 1)
│   │
│   └── RegistrationSuccessScreen.tsx         # Đăng ký thành công
│                                             # - Hiển thị thông tin đã đăng ký:
│                                             #   + Household ID
│                                             #   + User ID
│                                             #   + Subscription ID
│                                             # - Button: "Đăng nhập ngay"
│                                             # - Redirect đến LoginScreen
```

---

## 📱 ADMIN ROLE (Quản trị viên)

### Dashboard & Analytics
```
screens/
├── admin/
│   ├── dashboard/
│   │   ├── AdminDashboardScreen.tsx          # F004: view_platform_analytics
│   │   └── PlatformAnalyticsScreen.tsx       # F004: view_platform_analytics
│   │
│   ├── subscriptions/
│   │   ├── SubscriptionListScreen.tsx        # F003: manage_subscriptions (List all)
│   │   │                                     # - GET /api/admin/subscriptions
│   │   │                                     # - Hiển thị tất cả subscriptions (all households)
│   │   │                                     # - Filter: household_id, plan_id, is_active, date range
│   │   │                                     # - Action: Deactivate subscription (CHỈ deactivate, không edit plan_id)
│   │   │
│   │   └── SubscriptionDeactivateScreen.tsx  # F003: manage_subscriptions (Deactivate only)
│   │                                         # - PUT /api/admin/subscriptions/<id>
│   │                                         # - CHỈ được deactivate (is_active=false)
│   │                                         # - KHÔNG được: Create, Update plan_id, Delete
│   │                                         # - KHÔNG được: Activate (Owner tự activate khi upgrade)
│   │
│   ├── subscription-plans/
│   │   ├── SubscriptionPlanListScreen.tsx    # F002: manage_subscription_plans (List)
│   │   ├── SubscriptionPlanDetailScreen.tsx  # F002: manage_subscription_plans (Detail)
│   │   ├── SubscriptionPlanCreateScreen.tsx  # F002: manage_subscription_plans (Create)
│   │   └── SubscriptionPlanEditScreen.tsx    # F002: manage_subscription_plans (Update)
│   │
│   ├── users/
│   │   ├── UserListScreen.tsx                # F005: manage_admin_users (List)
│   │   ├── UserDetailScreen.tsx              # F005: manage_admin_users (Detail)
│   │   ├── UserCreateScreen.tsx              # F005: manage_admin_users (Create)
│   │   └── UserEditScreen.tsx                # F005: manage_admin_users (Update)
│   │
│   ├── accounting/
│   │   ├── AccountingLedgerListScreen.tsx    # F007: view_all_accounting_ledgers
│   │   ├── AccountingLedgerExportScreen.tsx  # F007: Export reports
│   │   └── AccountingLedgerDetailScreen.tsx  # F007: View detail
│   │
│   ├── system-config/
│   │   ├── SystemConfigScreen.tsx            # F006: manage_system_config (View)
│   │   └── SystemConfigEditScreen.tsx        # F006: manage_system_config (Update)
│   │
│   └── roles-functions/
│       ├── RoleListScreen.tsx                # Admin: manage roles
│       ├── RoleDetailScreen.tsx
│       ├── FunctionListScreen.tsx            # Admin: manage functions
│       ├── FunctionDetailScreen.tsx
│       └── RoleFunctionAssignScreen.tsx      # Admin: assign functions to roles
```

---

## 🏪 OWNER ROLE (Chủ hộ kinh doanh)


### Dashboard & Home
```
screens/
├── owner/
│   ├── dashboard/
│   │   ├── OwnerDashboardScreen.tsx          # Overview: revenue, alerts, summary
│   │   └── HomeScreen.tsx                    # Quick access to main features
│   │
│   ├── household/
│   │   ├── HouseholdProfileScreen.tsx        # F102: view_own_household (View)
│   │   └── HouseholdEditScreen.tsx           # F102: view_own_household (Update)
│   │
│   ├── subscription/
│   │   ├── SubscriptionViewScreen.tsx        # F102: view_own_household (View subscription)
│   │   │                                     # - GET /api/owner/subscription
│   │   │                                     # - Hiển thị subscription của household mình
│   │   │                                     # - Thông tin: plan_id, start_date, end_date, is_active
│   │   │                                     # - Button: "Upgrade Plan" → SubscriptionUpgradeScreen
│   │   │
│   │   └── SubscriptionUpgradeScreen.tsx     # F102: view_own_household (Upgrade subscription)
│   │                                         # - GET /api/owner/subscription-plans (lấy danh sách plans active - F102: R)
│   │                                         #   * Owner đã login, cần permission check (F102)
│   │                                         #   * CHỈ trả về plans có status = "active"
│   │                                         # - Hiển thị danh sách plans:
│   │                                         #   ├── Plan ID
│   │                                         #   ├── Plan name
│   │                                         #   ├── Price
│   │                                         #   ├── Billing cycle (monthly/yearly)
│   │                                         #   └── Description
│   │                                         # - Chọn plan mới (plan_id)
│   │                                         # - PUT /api/owner/subscription (upgrade plan_id - F102: U)
│   │                                         # - System tự động: Update plan_id, start_date, end_date (tính từ billing_cycle)
│   │                                         # - Owner tự upgrade, không cần Admin
│   │
│   ├── employees/
│   │   ├── EmployeeListScreen.tsx            # F101: manage_employees (List)
│   │   ├── EmployeeDetailScreen.tsx          # F101: manage_employees (Detail)
│   │   ├── EmployeeCreateScreen.tsx          # F101: manage_employees (Create)
│   │   └── EmployeeEditScreen.tsx            # F101: manage_employees (Update)
│   │
│   ├── products/
│   │   ├── ProductListScreen.tsx             # F104: manage_products (List)
│   │   ├── ProductDetailScreen.tsx           # F104: manage_products (Detail)
│   │   ├── ProductCreateScreen.tsx           # F104: manage_products (Create)
│   │   └── ProductEditScreen.tsx             # F104: manage_products (Update)
│   │
│   ├── categories/
│   │   ├── CategoryListScreen.tsx            # F103: manage_categories (List)
│   │   ├── CategoryDetailScreen.tsx          # F103: manage_categories (Detail)
│   │   ├── CategoryCreateScreen.tsx          # F103: manage_categories (Create)
│   │   └── CategoryEditScreen.tsx            # F103: manage_categories (Update)
│   │
│   ├── units/
│   │   ├── UnitListScreen.tsx                # F105: manage_units (List)
│   │   ├── UnitDetailScreen.tsx              # F105: manage_units (Detail)
│   │   ├── UnitCreateScreen.tsx              # F105: manage_units (Create)
│   │   └── UnitEditScreen.tsx                # F105: manage_units (Update)
│   │
│   ├── warehouses/
│   │   ├── WarehouseListScreen.tsx           # F107: manage_warehouses (List)
│   │   ├── WarehouseDetailScreen.tsx         # F107: manage_warehouses (Detail)
│   │   ├── WarehouseCreateScreen.tsx         # F107: manage_warehouses (Create)
│   │   └── WarehouseEditScreen.tsx           # F107: manage_warehouses (Update)
│   │
│   ├── inventory/
│   │   ├── InventoryListScreen.tsx           # F106: manage_inventory (List)
│   │   ├── InventoryDetailScreen.tsx         # F106: manage_inventory (Detail)
│   │   ├── InventoryCreateScreen.tsx         # F106: manage_inventory (Create)
│   │   └── InventoryEditScreen.tsx           # F106: manage_inventory (Update)
│   │
│   ├── import-receipts/
│   │   ├── ImportReceiptListScreen.tsx       # F108: manage_import_receipts (List)
│   │   ├── ImportReceiptDetailScreen.tsx     # F108: manage_import_receipts (Detail)
│   │   ├── ImportReceiptCreateScreen.tsx     # F108: manage_import_receipts (Create)
│   │   ├── ImportReceiptEditScreen.tsx       # F108: manage_import_receipts (Update)
│   │   └── ImportReceiptConfirmScreen.tsx    # F108: Confirm import (tăng inventory)
│   │
│   ├── import-details/
│   │   ├── ImportDetailListScreen.tsx        # List details của import receipt
│   │   ├── ImportDetailCreateScreen.tsx      # Create detail
│   │   └── ImportDetailEditScreen.tsx        # Update detail
│   │
│   ├── export-receipts/
│   │   ├── ExportReceiptListScreen.tsx       # F118: manage_export_receipts (List)
│   │   ├── ExportReceiptDetailScreen.tsx     # F118: manage_export_receipts (Detail)
│   │   ├── ExportReceiptCreateScreen.tsx     # F118: manage_export_receipts (Create)
│   │   ├── ExportReceiptEditScreen.tsx       # F118: manage_export_receipts (Update)
│   │   └── ExportReceiptConfirmScreen.tsx    # F118: Confirm export (giảm inventory)
│   │
│   ├── export-details/
│   │   ├── ExportDetailListScreen.tsx        # List details của export receipt
│   │   ├── ExportDetailCreateScreen.tsx      # Create detail
│   │   └── ExportDetailEditScreen.tsx        # Update detail
│   │
│   ├── customers/
│   │   ├── CustomerListScreen.tsx            # F109: manage_customers (List)
│   │   ├── CustomerDetailScreen.tsx          # F109: manage_customers (Detail)
│   │   ├── CustomerCreateScreen.tsx          # F109: manage_customers (Create)
│   │   ├── CustomerEditScreen.tsx            # F109: manage_customers (Update)
│   │   ├── CustomerHistoryScreen.tsx         # View purchase history
│   │   └── CustomerDebtScreen.tsx            # View outstanding debt
│   │
│   ├── sellers/
│   │   ├── SellerListScreen.tsx              # F110: manage_sellers (List)
│   │   ├── SellerDetailScreen.tsx            # F110: manage_sellers (Detail)
│   │   ├── SellerCreateScreen.tsx            # F110: manage_sellers (Create)
│   │   └── SellerEditScreen.tsx              # F110: manage_sellers (Update)
│   │
│   ├── invoices/
│   │   ├── InvoiceListScreen.tsx             # F111: manage_all_invoices (List)
│   │   │                                     # - GET /api/owner/invoices (filter by status)
│   │   │                                     # - Hiển thị tất cả invoices của household
│   │   │                                     # - Filter: status (Draft, Confirm, Delete), date range
│   │   │
│   │   ├── InvoiceCreateScreen.tsx           # F111: manage_all_invoices (Create)
│   │   │                                     # - POST /api/owner/invoices
│   │   │                                     # - Tạo invoice + details trong 1 request (transaction)
│   │   │                                     # - Form: customer_id, seller_id, invoice_type, description
│   │   │                                     # - Details: product_id, unit_id, quantity, price, vat, discount
│   │   │                                     # - Tự động tính: total_amount, vat_total, discount_total
│   │   │
│   │   ├── InvoiceDetailScreen.tsx           # F111: manage_all_invoices (Detail)
│   │   │                                     # - GET /api/owner/invoices/<id>
│   │   │                                     # - GET /api/owner/invoices/<id>/details
│   │   │
│   │   ├── InvoiceEditScreen.tsx             # F111: manage_all_invoices (Update)
│   │   │                                     # - PUT /api/owner/invoices/<id>
│   │   │                                     # - Chỉ được update khi status='Draft'
│   │   │
│   │   ├── InvoiceConfirmScreen.tsx          # F111: Confirm invoice
│   │   │                                     # - PUT /api/owner/invoices/<id>/confirm
│   │   │                                     # - Bất kỳ ai trong household đều có thể confirm
│   │   │
│   │   └── InvoicePrintScreen.tsx           # F111: Print invoice
│   │                                         # - GET /api/owner/invoices/<id>/print
│   │                                         # - Trả về invoice + tất cả details để in
│   │
│   ├── invoice-details/
│   │   ├── InvoiceDetailListScreen.tsx       # List invoice details
│   │   │                                     # - GET /api/invoices/<invoice_id>/details
│   │   │
│   │   ├── InvoiceDetailCreateScreen.tsx     # Create invoice detail
│   │   │                                     # - POST /api/invoices/<invoice_id>/details
│   │   │                                     # - Chỉ được tạo khi invoice status='Draft'
│   │   │
│   │   └── InvoiceDetailEditScreen.tsx       # Update invoice detail
│   │                                         # - PUT /api/invoices/<invoice_id>/details/<id>
│   │                                         # - DELETE /api/invoices/<invoice_id>/details/<id>
│   │                                         # - Chỉ được update/delete khi invoice status='Draft'
│   │
│   ├── payments/
│   │   ├── PaymentListScreen.tsx             # F112: manage_payments (List)
│   │   ├── PaymentDetailScreen.tsx           # F112: manage_payments (Detail)
│   │   ├── PaymentCreateScreen.tsx           # F112: manage_payments (Create)
│   │   └── PaymentEditScreen.tsx             # F112: manage_payments (Update)
│   │
│   ├── payment-methods/
│   │   ├── PaymentMethodListScreen.tsx       # F113: manage_payment_methods (List)
│   │   ├── PaymentMethodDetailScreen.tsx     # F113: manage_payment_methods (Detail)
│   │   ├── PaymentMethodCreateScreen.tsx     # F113: manage_payment_methods (Create)
│   │   └── PaymentMethodEditScreen.tsx       # F113: manage_payment_methods (Update)
│   │
│   ├── debt-records/
│   │   ├── DebtRecordListScreen.tsx          # F114: manage_debt_records (List)
│   │   ├── DebtRecordDetailScreen.tsx        # F114: manage_debt_records (Detail)
│   │   ├── DebtRecordCreateScreen.tsx        # F114: manage_debt_records (Create)
│   │   └── DebtRecordEditScreen.tsx          # F114: manage_debt_records (Update)
│   │
│   ├── reports/
│   │   ├── ReportDashboardScreen.tsx         # F115: view_household_reports
│   │   ├── DailyRevenueReportScreen.tsx      # Daily revenue report
│   │   ├── MonthlyRevenueReportScreen.tsx    # Monthly revenue report
│   │   ├── OutstandingDebtReportScreen.tsx   # Outstanding debt report
│   │   └── BestSellersReportScreen.tsx       # Top-selling products
│   │
│   └── accounting/
│       ├── AccountingLedgerListScreen.tsx    # F116: view_accounting_ledgers
│       ├── AccountingLedgerExportScreen.tsx  # F117: export_reports (Excel)
│       └── AccountingLedgerDetailScreen.tsx  # View detail
```

**Lưu ý:** Owner có tất cả chức năng của Employee (xem phần Employee bên dưới)

---

## 👤 EMPLOYEE ROLE (Nhân viên)

### Main Features
```
screens/
├── employee/
│   ├── dashboard/
│   │   ├── EmployeeHomeScreen.tsx            # Quick access screen
│   │   └── NotificationCenterScreen.tsx      # F215: receive_notifications
│   │
│   ├── products/
│   │   ├── ProductListScreen.tsx             # F201: view_products (Read-only)
│   │   └── ProductDetailScreen.tsx           # F201: view_products (Read-only)
│   │
│   ├── categories/
│   │   └── CategoryListScreen.tsx            # F202: view_categories (Read-only)
│   │
│   ├── units/
│   │   └── UnitListScreen.tsx                # F204: view_units (Read-only)
│   │
│   ├── inventory/
│   │   ├── InventoryListScreen.tsx           # F203: view_inventory (Read-only)
│   │   └── InventoryDetailScreen.tsx         # F203: Check stock by product/warehouse
│   │
│   ├── customers/
│   │   ├── CustomerListScreen.tsx            # F205: view_customers (Read-only)
│   │   ├── CustomerDetailScreen.tsx          # F205: view_customers (Read-only)
│   │   └── CustomerDebtScreen.tsx            # F206: view_customer_debt
│   │
│   ├── invoices/
│   │   ├── InvoiceListScreen.tsx            # F208: view_invoices
│   │   │                                     # - GET /api/employee/invoices (filter by status)
│   │   │                                     # - Hiển thị tất cả invoices của household
│   │   │                                     # - Filter: status='Draft' để xem draft orders từ AI
│   │   │                                     # - Không phân biệt ai tạo, chỉ filter theo household_id
│   │   │
│   │   ├── InvoiceCreateScreen.tsx          # F207: create_sales_invoice
│   │   │                                     # - POST /api/employee/invoices
│   │   │                                     # - Tạo invoice + details trong 1 request (transaction)
│   │   │                                     # - Search products (F201)
│   │   │                                     # - Add to cart (details)
│   │   │                                     # - Select customer (optional) (F205)
│   │   │                                     # - Check customer debt (F206)
│   │   │                                     # - Record debt if on credit (F212)
│   │   │                                     # - Tự động tính: total_amount, vat_total, discount_total
│   │   │                                     # - Status: 'Draft' (mặc định)
│   │   │
│   │   ├── InvoiceDetailScreen.tsx          # F208: View invoice detail
│   │   │                                     # - GET /api/employee/invoices/<id>
│   │   │                                     # - GET /api/employee/invoices/<id>/details
│   │   │
│   │   ├── InvoiceEditScreen.tsx            # F209: update_draft_invoice
│   │   │                                     # - PUT /api/employee/invoices/<id>
│   │   │                                     # - Chỉ được update khi status='Draft'
│   │   │
│   │   ├── InvoiceConfirmScreen.tsx         # F210: confirm_invoice
│   │   │                                     # - PUT /api/employee/invoices/<id>/confirm
│   │   │                                     # - Bất kỳ ai trong household đều có thể confirm
│   │   │                                     # - Không cần là người tạo
│   │   │                                     # - Auto deduct inventory
│   │   │                                     # - Auto create debt record (if on credit)
│   │   │                                     # - Auto update accounting ledger
│   │   │
│   │   └── InvoicePrintScreen.tsx           # Print invoice
│   │                                         # - GET /api/employee/invoices/<id>/print
│   │                                         # - Trả về invoice + tất cả details để in
│   │
│   ├── invoice-details/
│   │   ├── InvoiceDetailListScreen.tsx       # List invoice details
│   │   │                                     # - GET /api/invoices/<invoice_id>/details
│   │   │
│   │   ├── InvoiceDetailCreateScreen.tsx     # Create invoice detail
│   │   │                                     # - POST /api/invoices/<invoice_id>/details
│   │   │                                     # - Chỉ được tạo khi invoice status='Draft'
│   │   │
│   │   └── InvoiceDetailEditScreen.tsx       # Update invoice detail
│   │                                         # - PUT /api/invoices/<invoice_id>/details/<id>
│   │                                         # - DELETE /api/invoices/<invoice_id>/details/<id>
│   │                                         # - Chỉ được update/delete khi invoice status='Draft'
│   │
│   ├── payments/
│   │   ├── PaymentCreateScreen.tsx           # F211: record_payment
│   │   └── PaymentDetailScreen.tsx           # F211: view payment
│   │
│   ├── debt-records/
│   │   ├── DebtRecordCreateScreen.tsx        # F212: record_debt
│   │   └── DebtRecordDetailScreen.tsx        # F212: view debt record
│   │
│   └── print/
│       └── InvoicePrintScreen.tsx            # Print sales orders
```

---

## 🔄 SHARED SCREENS (Dùng chung cho nhiều Role)

### Common Components
```
components/
├── common/
│   ├── Header.tsx
│   ├── Sidebar.tsx
│   ├── SearchBar.tsx
│   ├── DataTable.tsx
│   ├── FormInput.tsx
│   ├── DatePicker.tsx
│   ├── StatusBadge.tsx
│   └── ConfirmDialog.tsx
│
├── invoice/
│   ├── InvoiceForm.tsx
│   ├── InvoiceDetailForm.tsx
│   ├── InvoiceSummary.tsx
│   └── InvoicePrintTemplate.tsx
│
├── product/
│   ├── ProductCard.tsx
│   ├── ProductSearch.tsx
│   └── ProductQuickAdd.tsx
│
├── customer/
│   ├── CustomerSelect.tsx
│   ├── CustomerInfo.tsx
│   └── DebtSummary.tsx
│
└── reports/
    ├── RevenueChart.tsx
    ├── DebtChart.tsx
    └── ExportButton.tsx
```

---

## 📊 NAVIGATION FLOW

### Admin Navigation
```
LoginScreen (chung)
  ↓
AdminDashboardScreen
  ├── Subscriptions
  │   └── SubscriptionListScreen → Deactivate (CHỈ list và deactivate, KHÔNG create/edit plan_id/delete)
  ├── Subscription Plans
  │   └── SubscriptionPlanListScreen → Detail → Create/Edit
  ├── Users
  │   └── UserListScreen → Detail → Create/Edit
  ├── Accounting Ledgers
  │   └── AccountingLedgerListScreen → Export
  └── System Config
      └── SystemConfigScreen → Edit
```

### Owner Navigation
```
LoginScreen (chung)
  ↓
OwnerDashboardScreen
  ├── Orders (same as Employee)
  ├── Products
  │   └── ProductListScreen → Detail → Create/Edit
  ├── Inventory
  │   ├── InventoryListScreen
  │   └── Import/Export Receipts
  ├── Customers
  │   └── CustomerListScreen → Detail → History → Debt
  ├── Reports
  │   ├── Daily/Monthly Revenue
  │   ├── Outstanding Debt
  │   └── Best Sellers
  ├── Accounting
  │   └── AccountingLedgerListScreen → Export
  ├── Employees
  │   └── EmployeeListScreen → Create/Edit
  ├── Subscription
  │   └── SubscriptionViewScreen → Upgrade (F102: view_own_household - R, U)
  │       # GET /api/owner/subscription (xem subscription của household mình)
  │       # PUT /api/owner/subscription (upgrade plan_id - tự upgrade, không cần Admin)
  └── Settings
      └── HouseholdProfileScreen → Edit (F102: view_own_household - R, U)
```

### Employee Navigation
```
LoginScreen (chung)
  ↓
EmployeeHomeScreen
  ├── Create Order
  │   └── OrderCreateScreen
  │       ├── Search Products
  │       ├── Add to Cart
  │       ├── Select Customer
  │       ├── Record Debt (if on credit)
  │       └── Create Draft → Confirm
  │
  ├── View Invoices
  │   └── InvoiceListScreen → Detail → Edit → Confirm
  │       └── Filter status='Draft' để xem draft orders từ AI
  │
  ├── Products (View Only)
  │   └── ProductListScreen → Detail
  │
  ├── Inventory (View Only)
  │   └── InventoryListScreen → Check Stock
  │
  ├── Customers (View Only)
  │   └── CustomerListScreen → Detail → View Debt
  │
  ├── Record Payment
  │   └── PaymentCreateScreen
  │
  ├── Record Debt
  │   └── DebtRecordCreateScreen
  │
  └── Notifications
      └── NotificationCenterScreen
```

---

## 🎯 KEY USER FLOWS

### Flow 0: Owner đăng ký tài khoản
```
1. LandingScreen / WelcomeScreen
   ↓
2. SubscriptionPlanSelectionScreen (registration/)
   ├── GET /api/public/subscription-plans (Public endpoint, không cần auth)
   ├── Hiển thị danh sách subscription plans (active only)
   ├── So sánh các gói (Basic, Pro, Premium, etc.)
   ├── Chọn gói đăng ký
   └── Lưu plan_id
   ↓
3. HouseholdRegistrationScreen (registration/)
   ├── Điền thông tin hộ kinh doanh:
   │   ├── Tên hộ kinh doanh (name) - required
   │   ├── Mã số thuế (tax_code) - CCCD người đại diện (optional, unique)
   │   ├── Số điện thoại (phone) - optional
   │   ├── Địa chỉ (address) - optional
   │   └── Mô tả (description - optional)
   ├── Validation: check tax_code unique (nếu có)
   └── Lưu household data (chưa tạo, chờ bước 4)
   ↓
4. OwnerAccountCreationScreen (registration/)
   ├── Điền thông tin tài khoản:
   │   ├── Username (user_name) - required, unique
   │   ├── Password (password) - required
   │   ├── Confirm Password
   │   ├── Email (optional)
   │   └── Description (optional)
   ├── POST /api/public/register (Public endpoint, không cần auth)
   │   Request body:
   │   {
   │     "plan_id": <từ bước 2>,
   │     "household": { <từ bước 3> },
   │     "owner_account": { <từ form này> }
   │   }
   │   └── Tạo tất cả trong 1 transaction:
   │       ├── Tạo Household record
   │       ├── Tạo User record với role Owner (link với household)
   │       └── Tạo Subscription record:
   │           ├── plan_id: từ bước 2
   │           ├── household_id: từ household vừa tạo
   │           ├── start_date: today
   │           ├── end_date: start_date + plan duration (dựa trên billing_cycle)
   │           └── is_active: true
   ↓
5. RegistrationSuccessScreen (registration/)
   ├── Hiển thị thông tin đã đăng ký:
   │   ├── Household ID
   │   ├── User ID
   │   └── Subscription ID
   └── Button: "Đăng nhập ngay"
   ↓
6. LoginScreen (auth/) - chung cho tất cả roles
   └── Login với username/password vừa tạo
   └── Auto detect role → Redirect:
       ├── Admin → AdminDashboardScreen
       ├── Owner → OwnerDashboardScreen
       └── Employee → EmployeeHomeScreen
   ↓
7. OwnerDashboardScreen
   └── Owner có thể quản lý household của mình qua F102: view_own_household (R, U)
```

### Flow 1: Employee tạo đơn bán hàng
```
1. EmployeeHomeScreen
   ↓
2. InvoiceCreateScreen (employee/invoices/)
   ├── Search Products (F201)
   ├── Add to Cart (details: product_id, unit_id, quantity, price, vat, discount)
   ├── Select Customer (optional) (F205)
   ├── Check Customer Debt (F206)
   ├── POST /api/employee/invoices
   │   └── Tạo invoice + details trong 1 transaction
   │   └── Status: 'Draft' (mặc định)
   │   └── Tự động tính: total_amount, vat_total, discount_total từ details
   ↓
3. InvoiceEditScreen (if needed) (F209)
   ├── PUT /api/employee/invoices/<id>
   └── Chỉ được update khi status='Draft'
   ↓
4. InvoiceConfirmScreen (F210)
   ├── PUT /api/employee/invoices/<id>/confirm
   ├── Bất kỳ ai trong household đều có thể confirm
   ├── Auto deduct inventory
   ├── Auto create debt record (if on credit) (F212)
   ├── Auto update accounting ledger
   └── Status: 'Draft' → 'Confirm'
   ↓
5. InvoicePrintScreen
   └── GET /api/employee/invoices/<id>/print
```

### Flow 2: AI tạo draft order (gộp vào Flow 1)
```
1. AI receives message (text/voice)
   ↓
2. Generate draft order (tạo invoice với status='Draft', source='AI')
   ├── POST /api/employee/invoices (hoặc endpoint riêng cho AI)
   └── Tạo invoice + details trong 1 transaction
   ↓
3. NotificationCenterScreen (F215) - Real-time notification
   ↓
4. InvoiceListScreen (employee/invoices/)
   ├── GET /api/employee/invoices?status=Draft
   └── Hiển thị draft orders (filter status='Draft' để xem draft orders từ AI)
   ↓
5. InvoiceDetailScreen - Review
   ├── GET /api/employee/invoices/<id>
   └── GET /api/employee/invoices/<id>/details
   ↓
6. InvoiceConfirmScreen (F210)
   ├── PUT /api/employee/invoices/<id>/confirm
   ├── Bất kỳ ai trong household đều có thể confirm
   ├── Auto deduct inventory
   └── Auto update accounting ledger
```

### Flow 2.5: Owner upgrade subscription plan
```
1. OwnerDashboardScreen
   ↓
2. SubscriptionViewScreen (owner/subscription/)
   ├── GET /api/owner/subscription (F102: R)
   ├── Hiển thị subscription hiện tại:
   │   ├── Plan ID hiện tại
   │   ├── Plan name hiện tại
   │   ├── Start date
   │   ├── End date
   │   └── Status (is_active)
   ├── Button: "Upgrade Plan" → SubscriptionUpgradeScreen
   └── Button: "View Household" → HouseholdProfileScreen
   ↓
3. SubscriptionUpgradeScreen (owner/subscription/)
   ├── GET /api/owner/subscription-plans (F102: R - Owner đã login, có permission check)
   ├── Hiển thị danh sách plans:
   │   ├── Plan ID
   │   ├── Plan name
   │   ├── Price
   │   ├── Billing cycle (monthly/yearly)
   │   └── Description
   ├── Chọn plan mới (plan_id)
   ├── PUT /api/owner/subscription
   │   Request body:
   │   {
   │     "plan_id": <plan_id mới>
   │   }
   │   └── System tự động:
   │       ├── Update plan_id
   │       ├── Update start_date (default: today)
   │       └── Update end_date (tính từ billing_cycle của plan mới)
   └── Success message: "Upgrade thành công"
   ↓
4. SubscriptionViewScreen (refresh)
   └── Hiển thị subscription mới với plan_id mới
```

### Flow 3: Owner xem báo cáo
```
1. OwnerDashboardScreen
   ↓
2. ReportDashboardScreen (F115)
   ├── DailyRevenueReportScreen
   ├── MonthlyRevenueReportScreen
   ├── OutstandingDebtReportScreen
   └── BestSellersReportScreen
   ↓
3. AccountingLedgerListScreen (F116)
   ↓
4. AccountingLedgerExportScreen (F117)
   └── Export Excel (Circular 88/2021/TT-BTC)
```

### Flow 4: Owner quản lý nhập hàng
```
1. OwnerDashboardScreen
   ↓
2. ImportReceiptListScreen (F108)
   ↓
3. ImportReceiptCreateScreen
   ├── Add Import Details
   └── Save as Draft
   ↓
4. ImportReceiptConfirmScreen
   ├── Confirm import
   ├── Auto increase inventory
   └── Auto update accounting ledger
```

---

## 📝 NOTES

1. **Owner Registration Flow** - Flow đăng ký Owner gồm 3 bước (Public, không cần auth):
   - Bước 1: Chọn Subscription Plan (GET /api/public/subscription-plans - lấy danh sách active plans)
   - Bước 2: Điền thông tin Household (name, tax_code, phone, address, description)
   - Bước 3: Tạo Owner account (POST /api/public/register - tạo tất cả trong 1 transaction:
     * Tạo Household
     * Tạo Owner User account (role Owner, link với household)
     * Tạo Subscription với plan đã chọn
   - Sau khi đăng ký thành công, tự động redirect đến LoginScreen

2. **Admin KHÔNG có quyền quản lý Household** - F001 manage_households đã bị xóa khỏi Admin functions.
   - Admin chỉ quản lý: Subscription Plans (F002), Subscriptions (F003 - CHỈ list và deactivate), Users (F005), Analytics (F004), System Config (F006), Accounting Ledgers (F007)
   - Chỉ Owner có quyền quản lý Household của chính mình qua F102: view_own_household (R, U)
   
3. **Admin quản lý Subscription (F003)** - CHỈ được list all subscriptions và deactivate:
   - GET /api/admin/subscriptions - List all subscriptions (CHỈ list, không create)
   - PUT /api/admin/subscriptions/<id> - Deactivate subscription (CHỈ deactivate is_active=false, KHÔNG được update plan_id)
   - **KHÔNG được**: Create subscription (Owner tự đăng ký), Update plan_id (Owner tự upgrade), Delete subscription, Activate subscription
   - Owner tự quản lý subscription: GET /api/owner/subscription (xem), PUT /api/owner/subscription (upgrade plan_id)

2. **Owner có tất cả chức năng của Employee** - Owner có thể tạo order, confirm invoice, etc.

2. **Real-time Notifications** - Dùng WebSocket hoặc polling để hiển thị draft orders từ AI

3. **Print Templates** - Sử dụng template theo Circular 88/2021/TT-BTC cho invoices và reports

4. **Search & Filter** - Tất cả list screens đều có search và filter functionality

5. **Keyboard Shortcuts** - OrderCreateScreen hỗ trợ keyboard shortcuts cho fast operations

6. **Offline Support** - Có thể cần cache data cho offline mode (mobile app)

7. **Image Upload** - ProductCreateScreen/EditScreen hỗ trợ upload product images

8. **Barcode Scanning** - Có thể tích hợp barcode scanner cho product search (nếu có hardware)
9. **Hiển thị vai trò** - Ở trang Home Screen hiển thị Vai trò tương ứng.
