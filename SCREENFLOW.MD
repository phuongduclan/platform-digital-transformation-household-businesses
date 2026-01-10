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

### Registration Flow (Chỉ cho Owner)
```
screens/
├── registration/
│   ├── SubscriptionPlanSelectionScreen.tsx    # Bước 1: Chọn gói đăng ký
│   │                                         # - Hiển thị danh sách subscription plans
│   │                                         # - So sánh các gói (Basic, Pro, etc.)
│   │                                         # - Chọn gói đăng ký
│   │
│   ├── HouseholdRegistrationScreen.tsx       # Bước 2: Điền thông tin hộ kinh doanh
│   │                                         # - Tên hộ kinh doanh (name)
│   │                                         # - Mã số thuế (tax_code) - CCCD người đại diện
│   │                                         # - Số điện thoại (phone)
│   │                                         # - Địa chỉ (address)
│   │                                         # - Mô tả (description)
│   │                                         # - Status (default: Active)
│   │
│   ├── OwnerAccountCreationScreen.tsx        # Bước 3: Tạo tài khoản Owner
│   │                                         # - Username (user_name)
│   │                                         # - Password (password)
│   │                                         # - Confirm Password
│   │                                         # - Email (optional)
│   │                                         # - Role: Owner (auto-assign)
│   │                                         # - Household ID (link to household vừa tạo)
│   │                                         # - Tạo subscription với plan đã chọn
│   │
│   └── RegistrationSuccessScreen.tsx         # Đăng ký thành công
│                                             # - Hiển thị thông tin đã đăng ký
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
│   ├── households/
│   │   ├── HouseholdListScreen.tsx           # F001: manage_households (List)
│   │   ├── HouseholdDetailScreen.tsx         # F001: manage_households (Detail)
│   │   ├── HouseholdCreateScreen.tsx         # F001: manage_households (Create)
│   │   └── HouseholdEditScreen.tsx           # F001: manage_households (Update)
│   │
│   ├── subscriptions/
│   │   ├── SubscriptionListScreen.tsx        # F003: manage_subscriptions (List)
│   │   ├── SubscriptionDetailScreen.tsx      # F003: manage_subscriptions (Detail)
│   │   ├── SubscriptionCreateScreen.tsx      # F003: manage_subscriptions (Create)
│   │   └── SubscriptionEditScreen.tsx        # F003: manage_subscriptions (Update)
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
│   │   ├── InvoiceDetailScreen.tsx           # F111: manage_all_invoices (Detail)
│   │   ├── InvoiceCreateScreen.tsx           # F111: manage_all_invoices (Create)
│   │   ├── InvoiceEditScreen.tsx             # F111: manage_all_invoices (Update)
│   │   └── InvoicePrintScreen.tsx            # Print invoice
│   │
│   ├── invoice-details/
│   │   ├── InvoiceDetailListScreen.tsx       # List invoice details
│   │   ├── InvoiceDetailCreateScreen.tsx     # Create invoice detail
│   │   └── InvoiceDetailEditScreen.tsx       # Update invoice detail
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
│   ├── orders/
│   │   ├── OrderCreateScreen.tsx             # F207: create_sales_invoice
│   │   │                                     # - Search products
│   │   │                                     # - Add to cart
│   │   │                                     # - Select customer (optional)
│   │   │                                     # - Record debt if on credit
│   │   │                                     # - Create draft invoice
│   │   │
│   │   ├── OrderListScreen.tsx               # F208: view_own_invoices
│   │   ├── OrderDetailScreen.tsx             # F208: View invoice detail
│   │   ├── OrderEditScreen.tsx               # F209: update_draft_invoice
│   │   └── OrderConfirmScreen.tsx            # F210: confirm_invoice
│   │
│   ├── draft-orders/
│   │   ├── DraftOrderListScreen.tsx          # F213: view_draft_orders (from AI)
│   │   ├── DraftOrderDetailScreen.tsx        # View draft order detail
│   │   └── DraftOrderConfirmScreen.tsx       # F214: confirm_draft_order
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
  ├── Households
  │   └── HouseholdListScreen → Detail → Create/Edit
  ├── Subscriptions
  │   └── SubscriptionListScreen → Detail → Create/Edit
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
  └── Settings
      └── HouseholdProfileScreen → Edit
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
  ├── View Orders
  │   └── OrderListScreen → Detail → Edit → Confirm
  │
  ├── Draft Orders (from AI)
  │   └── DraftOrderListScreen → Detail → Confirm
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
   ├── Hiển thị danh sách subscription plans (từ Admin)
   ├── So sánh các gói (Basic, Pro, Premium, etc.)
   ├── Chọn gói đăng ký
   └── Lưu plan_id
   ↓
3. HouseholdRegistrationScreen (registration/)
   ├── Điền thông tin hộ kinh doanh:
   │   ├── Tên hộ kinh doanh (name)
   │   ├── Mã số thuế (tax_code) - CCCD người đại diện
   │   ├── Số điện thoại (phone)
   │   ├── Địa chỉ (address)
   │   └── Mô tả (description - optional)
   ├── Validation: check tax_code unique
   └── Tạo Household record
   ↓
4. OwnerAccountCreationScreen (registration/)
   ├── Điền thông tin tài khoản:
   │   ├── Username (user_name) - unique
   │   ├── Password (password)
   │   ├── Confirm Password
   │   └── Email (optional)
   ├── Auto-assign:
   │   ├── Role: Owner
   │   ├── Household ID: từ bước 3
   │   └── Status: Active
   ├── Tạo User record với role Owner
   └── Tạo Subscription record:
       ├── plan_id: từ bước 2
       ├── household_id: từ bước 3
       ├── start_date: today
       ├── end_date: start_date + plan duration
       └── is_active: true
   ↓
5. RegistrationSuccessScreen (registration/)
   ├── Hiển thị thông tin đã đăng ký
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
```

### Flow 1: Employee tạo đơn bán hàng
```
1. EmployeeHomeScreen
   ↓
2. OrderCreateScreen
   ├── Search Products (F201)
   ├── Add to Cart
   ├── Select Customer (optional) (F205)
   ├── Check Customer Debt (F206)
   ├── Create Draft Invoice (F207)
   ↓
3. OrderEditScreen (if needed) (F209)
   ↓
4. OrderConfirmScreen (F210)
   ├── Auto deduct inventory
   ├── Auto create debt record (if on credit)
   ├── Auto update accounting ledger
   ↓
5. InvoicePrintScreen
```

### Flow 2: AI tạo draft order
```
1. AI receives message (text/voice)
   ↓
2. Generate draft order
   ↓
3. NotificationCenterScreen (F215) - Real-time notification
   ↓
4. DraftOrderListScreen (F213)
   ↓
5. DraftOrderDetailScreen - Review
   ↓
6. DraftOrderConfirmScreen (F214)
   ├── Convert to Invoice
   ├── Auto deduct inventory
   └── Auto update accounting ledger
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

1. **Owner Registration Flow** - Flow đăng ký Owner gồm 3 bước:
   - Bước 1: Chọn Subscription Plan (lấy từ danh sách plans do Admin quản lý)
   - Bước 2: Điền thông tin Household (tạo household record)
   - Bước 3: Tạo Owner account (tạo user với role Owner, link với household, tạo subscription)
   - Sau khi đăng ký thành công, tự động redirect đến LoginScreen

2. **Owner có tất cả chức năng của Employee** - Owner có thể tạo order, confirm invoice, etc.

2. **Real-time Notifications** - Dùng WebSocket hoặc polling để hiển thị draft orders từ AI

3. **Print Templates** - Sử dụng template theo Circular 88/2021/TT-BTC cho invoices và reports

4. **Search & Filter** - Tất cả list screens đều có search và filter functionality

5. **Keyboard Shortcuts** - OrderCreateScreen hỗ trợ keyboard shortcuts cho fast operations

6. **Offline Support** - Có thể cần cache data cho offline mode (mobile app)

7. **Image Upload** - ProductCreateScreen/EditScreen hỗ trợ upload product images

8. **Barcode Scanning** - Có thể tích hợp barcode scanner cho product search (nếu có hardware)
9. **Hiển thị vai trò** - Ở trang Home Screen hiển thị Vai trò tương ứng.
