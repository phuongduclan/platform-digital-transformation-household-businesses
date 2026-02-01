# 📱 Platform Digital Transformation - Screens & Pages Architecture

## Overview
Nền tảng quản lý tài chính cho hộ kinh doanh và doanh nghiệp nhỏ với 3 role chính: **Admin**, **Owner** (Chủ hộ kinh doanh), **Employee** (Nhân viên).

Công nghệ: **Next.js 15** (React 18) + **TypeScript** + **Tailwind CSS** + **Chart.js** + **React PDF**

---

## 🏗️ FE Structure - Directory Tree

```
FE/
├── src/
│   ├── app/                           # Next.js App Router (File-based routing)
│   │   ├── (auth)/                    # 🔐 AUTHENTICATION ROUTES
│   │   │   ├── login/
│   │   │   │   └── page.tsx           # Login Page - Đăng nhập hệ thống
│   │   │   │       ├── User credentials (email/password)
│   │   │   │       ├── JWT token generation
│   │   │   │       └── Role-based redirect
│   │   │   │
│   │   │   └── [redirected routes after login]
│   │   │
│   │   ├── admin/                     # 👨‍💼 ADMIN DASHBOARD & MANAGEMENT
│   │   │   ├── layout.tsx             # Admin layout wrapper
│   │   │   ├── page.tsx               # Dashboard - Thống kê tổng quan
│   │   │   │   ├── Total owners
│   │   │   │   ├── Active subscriptions
│   │   │   │   ├── Subscription plans count
│   │   │   │   ├── Revenue this month (Chart)
│   │   │   │   └── Quick actions
│   │   │   │
│   │   │   ├── analytics/             # 📊 Admin Analytics & Reports
│   │   │   │   └── page.tsx           # Analytics Dashboard
│   │   │   │       ├── Revenue trends
│   │   │   │       ├── User growth chart
│   │   │   │       ├── Platform metrics
│   │   │   │       └── Export reports
│   │   │   │
│   │   │   ├── users/                 # 👥 User Management
│   │   │   │   ├── page.tsx           # Users List & Search
│   │   │   │   │   ├── Table: user_name, email, role, status, created_at
│   │   │   │   │   ├── Filter by role/status
│   │   │   │   │   ├── Search functionality
│   │   │   │   │   ├── Pagination
│   │   │   │   │   └── Delete/Activate user
│   │   │   │   │
│   │   │   │   ├── create/
│   │   │   │   │   └── page.tsx       # Create New User
│   │   │   │   │       ├── Form: username, email, password, role
│   │   │   │   │       ├── Role selection (Admin/Owner/Employee)
│   │   │   │   │       └── Submit & validate
│   │   │   │   │
│   │   │   │   └── [id]/
│   │   │   │       └── page.tsx       # User Detail & Edit
│   │   │   │           ├── View user profile
│   │   │   │           ├── Edit user info
│   │   │   │           ├── Change permissions
│   │   │   │           └── View user activity logs
│   │   │   │
│   │   │   ├── subscription-plans/    # 📋 Subscription Plans Management
│   │   │   │   ├── page.tsx           # Plans List
│   │   │   │   │   ├── Table: plan_name, price, features, status
│   │   │   │   │   ├── View active/inactive plans
│   │   │   │   │   └── Bulk actions
│   │   │   │   │
│   │   │   │   ├── create/
│   │   │   │   │   └── page.tsx       # Create Subscription Plan
│   │   │   │   │       ├── Form: name, price, duration, features
│   │   │   │   │       ├── Features checkbox list
│   │   │   │   │       └── Preview & publish
│   │   │   │   │
│   │   │   │   └── [id]/
│   │   │   │       └── page.tsx       # Edit Plan
│   │   │   │           ├── Update plan details
│   │   │   │           ├── Manage features
│   │   │   │           └── View subscriptions using this plan
│   │   │   │
│   │   │   ├── subscriptions/         # 💳 Subscriptions Management
│   │   │   │   ├── page.tsx           # Subscriptions List
│   │   │   │   │   ├── Table: owner_name, plan_name, start_date, end_date, status
│   │   │   │   │   ├── Filter by status (Active/Expired/Canceled)
│   │   │   │   │   ├── Renewal actions
│   │   │   │   │   └── Cancel subscription
│   │   │   │   │
│   │   │   │   └── [id]/
│   │   │   │       └── page.tsx       # Subscription Detail
│   │   │   │           ├── Subscription info & timeline
│   │   │   │           ├── Invoice history
│   │   │   │           ├── Renew/cancel options
│   │   │   │           └── Owner contact info
│   │   │   │
│   │   │   ├── payment-methods/       # 💰 Payment Methods
│   │   │   │   └── page.tsx           # Payment Methods Configuration
│   │   │   │       ├── List: method_type, status, test_mode
│   │   │   │       ├── Add payment gateway
│   │   │   │       ├── Configure API keys (masked)
│   │   │   │       └── Test transaction
│   │   │   │
│   │   │   ├── config/                # ⚙️ Platform Configuration
│   │   │   │   └── page.tsx           # System Settings
│   │   │   │       ├── General settings
│   │   │   │       ├── Email configuration
│   │   │   │       ├── API settings
│   │   │   │       └── Feature flags
│   │   │   │
│   │   │   └── settings/              # 🔧 Admin Settings
│   │   │       └── page.tsx           # Admin Account Settings
│   │   │           ├── Profile management
│   │   │           ├── Change password
│   │   │           ├── Notification preferences
│   │   │           └── Activity logs
│   │   │
│   │   │
│   │   ├── owner/                     # 🏪 OWNER/BUSINESS DASHBOARD & MANAGEMENT
│   │   │   ├── layout.tsx             # Owner layout wrapper with sidebar
│   │   │   ├── page.tsx               # Dashboard - Kinh doanh tổng quan
│   │   │   │   ├── Today revenue (KPI Card)
│   │   │   │   ├── Month revenue (KPI Card)
│   │   │   │   ├── Total invoices count
│   │   │   │   ├── Outstanding debt (Chart)
│   │   │   │   ├── Revenue trend chart (Line chart)
│   │   │   │   ├── Debt trend chart
│   │   │   │   ├── Recent invoices table
│   │   │   │   └── Quick action buttons
│   │   │   │
│   │   │   ├── household/             # 🏠 Household Management
│   │   │   │   └── page.tsx           # Household Info & Settings
│   │   │   │       ├── Household name & address
│   │   │   │       ├── Edit address with autocomplete (Goong API)
│   │   │   │       ├── Business type & description
│   │   │   │       ├── Contact info
│   │   │   │       └── Save changes
│   │   │   │
│   │   │   ├── invoices/              # 📄 Invoice Management
│   │   │   │   ├── page.tsx           # Invoices List (Pro List UI)
│   │   │   │   │   ├── Table: invoice_no, customer, amount, status, date
│   │   │   │   │   ├── Filter by status (Draft/Issued/Paid/Overdue)
│   │   │   │   │   ├── Search by invoice_no/customer
│   │   │   │   │   ├── Pagination & sorting
│   │   │   │   │   ├── Bulk actions (print, export)
│   │   │   │   │   └── Status badges with colors
│   │   │   │   │
│   │   │   │   ├── create/
│   │   │   │   │   └── page.tsx       # Create New Invoice
│   │   │   │   │       ├── Form: customer, items, tax, discount
│   │   │   │   │       ├── Item table with add/remove rows
│   │   │   │   │       ├── Price calculation
│   │   │   │   │       ├── Invoice template preview (PDF)
│   │   │   │   │       ├── Save as draft or issue
│   │   │   │   │       └── AI-powered item suggestion (ai-button)
│   │   │   │   │
│   │   │   │   └── [id]/
│   │   │   │       └── page.tsx       # Invoice Detail & Edit
│   │   │   │           ├── View invoice (Read-only if issued)
│   │   │   │           ├── Edit invoice (if draft)
│   │   │   │           ├── Generate PDF
│   │   │   │           ├── Send to customer (email)
│   │   │   │           ├── Print preview
│   │   │   │           ├── Mark as paid
│   │   │   │           └── Delete invoice
│   │   │   │
│   │   │   ├── payments/              # 💳 Payment Recording
│   │   │   │   ├── page.tsx           # Payments List
│   │   │   │   │   ├── Table: invoice_no, customer, amount, method, date
│   │   │   │   │   ├── Filter by method/status
│   │   │   │   │   ├── Search functionality
│   │   │   │   │   └── View linked invoices
│   │   │   │   │
│   │   │   │   ├── create/
│   │   │   │   │   └── page.tsx       # Record New Payment
│   │   │   │   │       ├── Form: invoice, amount, method, date, note
│   │   │   │   │       ├── Method selection (Cash/Bank/Check)
│   │   │   │   │       ├── Auto-populate from invoice
│   │   │   │   │       └── Save payment record
│   │   │   │   │
│   │   │   │   └── [id]/
│   │   │   │       └── page.tsx       # Payment Detail & Edit
│   │   │   │           ├── View payment details
│   │   │   │           ├── Edit payment (if unconfirmed)
│   │   │   │           ├── View linked invoice
│   │   │   │           └── Delete payment
│   │   │   │
│   │   │   ├── debt-records/          # 💰 Debt Records / Aging Analysis
│   │   │   │   └── page.tsx           # Debt Records List
│   │   │   │       ├── Table: customer, amount, days_overdue, status
│   │   │   │       ├── Aging buckets (0-30, 30-60, 60-90, 90+)
│   │   │   │       ├── Total outstanding debt
│   │   │   │       ├── View customer transactions
│   │   │   │       └── Send collection reminder
│   │   │   │
│   │   │   ├── customers/             # 👥 Customer Management
│   │   │   │   ├── page.tsx           # Customers List
│   │   │   │   │   ├── Table: name, phone, email, total_purchases, outstanding_debt
│   │   │   │   │   ├── Search by name/phone
│   │   │   │   │   ├── Filter by status
│   │   │   │   │   └── Batch import/export
│   │   │   │   │
│   │   │   │   ├── create/
│   │   │   │   │   └── page.tsx       # Create New Customer
│   │   │   │   │       ├── Form: name, phone, email, address
│   │   │   │   │       ├── Address autocomplete (Goong API)
│   │   │   │   │       ├── Tax info
│   │   │   │   │       └── Save customer
│   │   │   │   │
│   │   │   │   └── [id]/
│   │   │   │       └── page.tsx       # Customer Detail & Edit
│   │   │   │           ├── View profile & transaction history
│   │   │   │           ├── Edit customer info
│   │   │   │           ├── View invoices & payments
│   │   │   │           ├── View outstanding balance
│   │   │   │           └── Send message
│   │   │   │
│   │   │   ├── sellers/               # 🛒 Seller Management
│   │   │   │   ├── page.tsx           # Sellers List
│   │   │   │   │   ├── Table: name, contact, total_purchases, outstanding_payable
│   │   │   │   │   ├── Filter & search
│   │   │   │   │   └── View transactions
│   │   │   │   │
│   │   │   │   ├── create/
│   │   │   │   │   └── page.tsx       # Create New Seller
│   │   │   │   │       ├── Form: name, phone, email, company, address
│   │   │   │   │       └── Save seller
│   │   │   │   │
│   │   │   │   └── [id]/
│   │   │   │       └── page.tsx       # Seller Detail
│   │   │   │           ├── View info & transactions
│   │   │   │           ├── Edit seller
│   │   │   │           └── View outstanding payables
│   │   │   │
│   │   │   ├── catalog/               # 📦 Catalog / Products Management
│   │   │   │   ├── page.tsx           # Products List
│   │   │   │   │   ├── Table: name, sku, category, unit_price, stock
│   │   │   │   │   ├── Filter by category/warehouse
│   │   │   │   │   ├── Search by name/sku
│   │   │   │   │   ├── Bulk import products
│   │   │   │   │   └── Export product list
│   │   │   │   │
│   │   │   │   ├── create/
│   │   │   │   │   └── page.tsx       # Create New Product
│   │   │   │   │       ├── Form: name, sku, category, price, stock
│   │   │   │   │       ├── Multiple UoM support
│   │   │   │   │       ├── Tax category selection
│   │   │   │   │       └── Save product
│   │   │   │   │
│   │   │   │   └── [id]/
│   │   │   │       └── page.tsx       # Edit Product
│   │   │   │           ├── Update product details
│   │   │   │           ├── Adjust stock
│   │   │   │           └── View stock movement history
│   │   │   │
│   │   │   ├── inventory/             # 📊 Inventory Management
│   │   │   │   └── page.tsx           # Inventory Overview
│   │   │   │       ├── Total items by warehouse
│   │   │   │       ├── Stock value
│   │   │   │       ├── Low stock alerts
│   │   │   │       ├── Movement chart
│   │   │   │       └── Inventory adjustment form
│   │   │   │
│   │   │   ├── warehouses/            # 🏭 Warehouse Management
│   │   │   │   ├── page.tsx           # Warehouses List
│   │   │   │   │   ├── Table: name, location, total_stock_value, status
│   │   │   │   │   └── View warehouse details
│   │   │   │   │
│   │   │   │   ├── create/
│   │   │   │   │   └── page.tsx       # Create New Warehouse
│   │   │   │   │       ├── Form: name, address, capacity
│   │   │   │   │       ├── Address autocomplete
│   │   │   │   │       └── Save warehouse
│   │   │   │   │
│   │   │   │   └── [id]/
│   │   │   │       └── page.tsx       # Warehouse Detail
│   │   │   │           ├── View inventory items
│   │   │   │           ├── Edit warehouse info
│   │   │   │           └── Transfer stock to other warehouses
│   │   │   │
│   │   │   ├── import-receipts/       # 📥 Import Records from Sellers
│   │   │   │   ├── page.tsx           # Imports List
│   │   │   │   │   ├── Table: receipt_no, seller, date, total_amount, status
│   │   │   │   │   ├── Filter by status (Draft/Received/Rejected)
│   │   │   │   │   └── View details
│   │   │   │   │
│   │   │   │   ├── create/
│   │   │   │   │   └── page.tsx       # Create Import Receipt
│   │   │   │   │       ├── Form: seller, items, quantity, unit_price
│   │   │   │   │       ├── Item table
│   │   │   │   │       ├── Calculate total
│   │   │   │   │       └── Save receipt
│   │   │   │   │
│   │   │   │   └── [id]/
│   │   │   │       └── page.tsx       # Import Detail
│   │   │   │           ├── View receipt details
│   │   │   │           ├── Edit (if draft)
│   │   │   │           ├── Confirm receipt
│   │   │   │           └── View in-stock items
│   │   │   │
│   │   │   ├── export-receipts/       # 📤 Export Records (Inventory Out)
│   │   │   │   ├── page.tsx           # Exports List
│   │   │   │   │   ├── Table: receipt_no, type, date, total_items, status
│   │   │   │   │   └── Filter & search
│   │   │   │   │
│   │   │   │   ├── create/
│   │   │   │   │   └── page.tsx       # Create Export Receipt
│   │   │   │   │       ├── Form: export_type, items, quantity
│   │   │   │   │       ├── Warehouse selection
│   │   │   │   │       ├── Reason selection
│   │   │   │   │       └── Save receipt
│   │   │   │   │
│   │   │   │   └── [id]/
│   │   │   │       └── page.tsx       # Export Detail
│   │   │   │           ├── View details
│   │   │   │           ├── Confirm export
│   │   │   │           └── Print barcode
│   │   │   │
│   │   │   ├── accounting-ledgers/    # 📈 Accounting Ledger (GL)
│   │   │   │   └── page.tsx           # General Ledger View
│   │   │   │       ├── Table: date, account, debit, credit, balance
│   │   │   │       ├── Filter by account/date range
│   │   │   │       ├── Trial balance report
│   │   │   │       └── Export to Excel
│   │   │   │
│   │   │   ├── reports/               # 📊 Reports & Analytics
│   │   │   │   └── page.tsx           # Reports Dashboard
│   │   │   │       ├── Sales report (by period/customer)
│   │   │   │       ├── Expense report
│   │   │   │       ├── Inventory valuation
│   │   │   │       ├── Customer aging report
│   │   │   │       ├── Supplier aging report
│   │   │   │       ├── Profit & loss statement
│   │   │   │       └── Export reports
│   │   │   │
│   │   │   ├── employees/             # 👥 Staff/Employee Management
│   │   │   │   ├── page.tsx           # Employees List
│   │   │   │   │   ├── Table: name, email, role, status, joined_date
│   │   │   │   │   ├── Filter by role
│   │   │   │   │   └── View employee details
│   │   │   │   │
│   │   │   │   ├── create/
│   │   │   │   │   └── page.tsx       # Invite New Employee
│   │   │   │   │       ├── Form: email, name, role
│   │   │   │   │       ├── Role selection (Sales/Warehouse/Manager)
│   │   │   │   │       ├── Permission checkboxes
│   │   │   │   │       └── Send invitation
│   │   │   │   │
│   │   │   │   └── [id]/
│   │   │   │       └── page.tsx       # Employee Detail
│   │   │   │           ├── View profile
│   │   │   │           ├── Edit permissions
│   │   │   │           ├── View activity log
│   │   │   │           └── Deactivate employee
│   │   │   │
│   │   │   ├── subscription-plans/    # 💳 Owner's Current Subscription
│   │   │   │   └── page.tsx           # Subscription Info & Upgrade
│   │   │   │       ├── Current plan details
│   │   │   │       ├── Features list
│   │   │   │       ├── Renewal date
│   │   │   │       ├── Available plans to upgrade
│   │   │   │       └── Upgrade button
│   │   │   │
│   │   │   └── settings/              # ⚙️ Business Settings
│   │   │       └── page.tsx           # Owner Account Settings
│   │   │           ├── Profile management
│   │   │           ├── Password change
│   │   │           ├── Notification preferences
│   │   │           ├── API keys (for integrations)
│   │   │           ├── Tax settings
│   │   │           ├── Payment method setup
│   │   │           └── Backup & export data
│   │   │
│   │   │
│   │   ├── employee/                  # 👷 EMPLOYEE DASHBOARD & LIMITED ACCESS
│   │   │   ├── layout.tsx             # Employee layout wrapper
│   │   │   ├── page.tsx               # Employee Dashboard
│   │   │   │   ├── Draft invoices count
│   │   │   │   ├── Customers in debt
│   │   │   │   ├── Total debt amount
│   │   │   │   ├── Draft invoices list
│   │   │   │   ├── Debt records list
│   │   │   │   └── Quick links to invoice creation
│   │   │   │
│   │   │   ├── customers/             # 👥 Customer Management (Limited)
│   │   │   │   └── page.tsx           # Customers List (View only)
│   │   │   │       ├── Table: name, phone, email
│   │   │   │       ├── View customer details
│   │   │   │       └── Search/filter
│   │   │   │
│   │   │   ├── debt-records/          # 💰 Debt Records (Read-only)
│   │   │   │   └── page.tsx           # Outstanding Debts
│   │   │   │       ├── List of customers owing money
│   │   │   │       ├── Amount & days overdue
│   │   │   │       ├── View aging report
│   │   │   │       └── Send reminder (if permitted)
│   │   │   │
│   │   │   ├── invoices/              # 📄 Invoice Management (Create/View)
│   │   │   │   ├── page.tsx           # Invoices List
│   │   │   │   │   ├── View all invoices
│   │   │   │   │   ├── Filter by status
│   │   │   │   │   └── View employee's created invoices
│   │   │   │   │
│   │   │   │   ├── create/
│   │   │   │   │   └── page.tsx       # Create Invoice (Limited)
│   │   │   │   │       ├── Form with customer & items
│   │   │   │   │       ├── AI-powered input helper
│   │   │   │   │       ├── Save as draft
│   │   │   │   │       └── Cannot publish without approval
│   │   │   │   │
│   │   │   │   └── [id]/
│   │   │   │       └── page.tsx       # View Invoice
│   │   │   │           ├── View invoice details
│   │   │   │           ├── Print invoice
│   │   │   │           └── Cannot modify if issued
│   │   │   │
│   │   │   ├── inventory/             # 📦 Inventory (Limited - View only)
│   │   │   │   └── page.tsx           # View Inventory
│   │   │   │       ├── View stock levels
│   │   │   │       ├── Cannot edit directly
│   │   │   │       └── View movement logs
│   │   │   │
│   │   │   └── settings/              # ⚙️ Employee Settings
│   │   │       └── page.tsx           # Employee Account Settings
│   │   │           ├── Profile management
│   │   │           ├── Change password
│   │   │           ├── Notification preferences
│   │   │           └── Activity log
│   │   │
│   │   │
│   │   ├── register/                  # 📝 Registration
│   │   │   └── page.tsx               # Business Registration Form
│   │   │       ├── Company name & type
│   │   │       ├── Owner details
│   │   │       ├── Address with autocomplete
│   │   │       ├── Email & phone
│   │   │       ├── Plan selection
│   │   │       └── Create account
│   │   │
│   │   ├── test-design/               # 🎨 Design Testing
│   │   │   └── [components for UI testing]
│   │   │
│   │   ├── layout.tsx                 # Root layout
│   │   ├── page.tsx                   # Landing page / redirects to role dashboard
│   │   ├── globals.css                # Global Tailwind styles
│   │   └── bizflow-loader.css         # Loading animation styles
│   │
│   ├── components/                    # Reusable React Components
│   │   ├── ui/                        # UI Components Library
│   │   │   ├── button.tsx             # Styled button component
│   │   │   ├── dialog.tsx             # Modal/Dialog (Radix)
│   │   │   ├── dropdown-menu.tsx      # Dropdown menu (Radix)
│   │   │   ├── form.tsx               # Form wrapper
│   │   │   ├── input.tsx              # Input field
│   │   │   ├── label.tsx              # Label component
│   │   │   ├── loading-overlay.tsx    # Loading spinner overlay
│   │   │   ├── toast.tsx              # Toast notification
│   │   │   ├── table.tsx              # Data table component
│   │   │   ├── card.tsx               # Card container
│   │   │   ├── pagination.tsx         # Pagination control
│   │   │   ├── select.tsx             # Select dropdown
│   │   │   ├── tabs.tsx               # Tab navigation
│   │   │   └── [more UI components]
│   │   │
│   │   ├── pdf/                       # PDF Components
│   │   │   ├── invoice-pdf.tsx        # Invoice PDF template
│   │   │   └── receipt-pdf.tsx        # Receipt PDF template
│   │   │
│   │   ├── address-autocomplete.tsx    # Goong API address autocomplete
│   │   ├── ai-button.tsx              # AI-powered input suggestions
│   │   ├── ai-invoice-input.tsx       # AI invoice item input
│   │   ├── invoice-template.tsx       # Invoice display template
│   │   ├── retail-invoice-template.tsx # Retail invoice template
│   │   └── loader.tsx                 # Loading component
│   │
│   ├── context/                       # React Context API
│   │   ├── auth-context.tsx           # Authentication state
│   │   ├── user-context.tsx           # User profile state
│   │   └── notification-context.tsx   # Notifications state
│   │
│   ├── services/                      # API Service Clients
│   │   ├── admin.service.ts           # Admin API calls
│   │   ├── owner.service.ts           # Owner API calls (Revenue, invoices, etc.)
│   │   ├── employee.service.ts        # Employee API calls
│   │   ├── auth.service.ts            # Authentication API
│   │   ├── invoice.service.ts         # Invoice operations
│   │   ├── payment.service.ts         # Payment operations
│   │   ├── customer.service.ts        # Customer CRUD
│   │   ├── product.service.ts         # Product CRUD
│   │   ├── inventory.service.ts       # Inventory operations
│   │   ├── warehouse.service.ts       # Warehouse CRUD
│   │   ├── report.service.ts          # Report generation
│   │   ├── api-client.ts              # Axios instance & interceptors
│   │   └── goong-service.ts           # Goong Maps API
│   │
│   ├── lib/                           # Utility Functions
│   │   ├── auth.ts                    # Auth helpers
│   │   ├── format.ts                  # Formatting utilities
│   │   ├── validators.ts              # Form validators
│   │   ├── constants.ts               # App constants
│   │   └── helpers.ts                 # Common helpers
│   │
│   └── types/                         # TypeScript Type Definitions
│       ├── user.ts                    # User types
│       ├── invoice.ts                 # Invoice types
│       ├── payment.ts                 # Payment types
│       ├── customer.ts                # Customer types
│       ├── product.ts                 # Product types
│       ├── api.ts                     # API response types
│       └── common.ts                  # Common types (pagination, status, etc.)
│
├── public/                            # Static assets
│   ├── images/
│   ├── icons/
│   └── logos/
│
├── next.config.js                     # Next.js config
├── tsconfig.json                      # TypeScript config
├── tailwind.config.ts                 # Tailwind CSS config
├── postcss.config.js                  # PostCSS config
└── package.json                       # Dependencies
```

---

## 🎯 Key Screen Features by Module

### 🔐 **Authentication Module**
- **Login Page**: JWT-based authentication with role selection
- **Registration**: Self-service business registration with subscription plan selection
- **Token Management**: 2-hour JWT token with household_id & permissions claims

### 👨‍💼 **Admin Module** 
- **Dashboard**: Platform-wide KPIs, revenue trends, user statistics
- **User Management**: CRUD operations, role assignment, status management
- **Subscription Plans**: Define, edit, manage subscription tiers
- **Subscriptions**: View all active/expired subscriptions, manage renewals
- **Payment Methods**: Configure payment gateways (Stripe, Zalopay, etc.)
- **Analytics**: Advanced platform analytics, revenue forecasts
- **Settings**: System configuration, email, API keys

### 🏪 **Owner Module** (Business Owner Dashboard)
- **Dashboard**: Today/month revenue, outstanding debt, invoice metrics, charts
- **Household**: Business info management with address autocomplete
- **Invoice Management**: Create, edit, issue, print invoices with PDF export
- **Payments**: Record payments, track payment methods, aging analysis
- **Customers**: Customer database, contact info, transaction history
- **Sellers**: Supplier management
- **Inventory**: Stock management, warehouse allocation
- **Accounting**: General ledger, trial balance, P&L
- **Reports**: Sales, expenses, inventory valuation, aging reports
- **Employees**: Staff management, role assignment, permission control
- **Settings**: Subscription management, payment setup, data export

### 👷 **Employee Module** (Limited Access)
- **Dashboard**: Draft invoices, customer debts, quick action links
- **Invoices**: Create (draft), view, search invoices
- **Customers**: View-only customer list
- **Debt Records**: View outstanding debts
- **Inventory**: View-only inventory access
- **Settings**: Personal account management

---

## 🔄 Data Flow Architecture

```
User Login (FE)
    ↓
Auth Service (FE) → Auth API (BE) → Database
    ↓
JWT Token + User Role
    ↓
Role-based Route Protection (FE)
    ↓
Dashboard Component
    ↓
Service Client (FE) → REST API (BE) → Repository → Database
    ↓
Display Data in Tables/Charts
    ↓
User Action (Create/Update/Delete)
    ↓
API Call with JWT Token
    ↓
Role-based Authorization Check (BE)
    ↓
Service Logic (Business Layer)
    ↓
Repository (Data Access)
    ↓
Update Database
    ↓
Response to FE
    ↓
Toast Notification + State Update
```

---

## 📡 Backend API Endpoints (Referenced in Services)

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/me` - Get current user profile
- `PUT /api/auth/me` - Update current user

### Admin
- `GET /api/admin/stats` - Dashboard statistics
- `GET /api/admin/analytics` - Analytics data
- `GET /api/admin/users` - List users (pagination)
- `POST /api/admin/users` - Create user
- `PUT /api/admin/users/{id}` - Update user
- `DELETE /api/admin/users/{id}` - Delete user
- `GET /api/admin/subscriptions` - List subscriptions
- `POST /api/admin/subscription-plans` - Create plan
- `GET /api/admin/payment-methods` - Payment gateway config

### Owner
- `GET /api/owner/dashboard/daily-revenue` - Today's revenue
- `GET /api/owner/dashboard/monthly-revenue` - Month revenue
- `GET /api/owner/dashboard/outstanding-debt` - Outstanding debt
- `GET /api/owner/invoices` - List invoices
- `POST /api/owner/invoices` - Create invoice
- `GET /api/owner/invoices/{id}` - Get invoice detail
- `PUT /api/owner/invoices/{id}` - Update invoice
- `DELETE /api/owner/invoices/{id}` - Delete invoice
- `GET /api/owner/customers` - List customers
- `POST /api/owner/customers` - Create customer
- `GET /api/owner/payments` - List payments
- `POST /api/owner/payments` - Record payment
- `GET /api/owner/debt-records` - Debt aging
- `GET /api/owner/inventory` - Inventory status
- `GET /api/owner/warehouses` - Warehouse list
- `POST /api/owner/warehouses` - Create warehouse
- `GET /api/owner/accounting-ledgers` - General ledger
- `GET /api/owner/employees` - List employees
- `POST /api/owner/employees` - Invite employee

### Employee
- `GET /api/employee/invoices` - List invoices
- `POST /api/employee/invoices` - Create invoice (draft)
- `GET /api/employee/customers` - List customers
- `GET /api/employee/debt-records` - View debts

### Shared APIs
- `POST /api/address/autocomplete` - Address autocomplete (Goong)
- `POST /api/address/detail` - Get address coordinates

---

## 🎨 UI Component Library

**Radix UI Base**: Dialog, Dropdown, Popover, Slot  
**Form Framework**: React Hook Form + Zod validation  
**Styling**: Tailwind CSS + class-variance-authority  
**Charts**: Chart.js + react-chartjs-2  
**PDF Export**: @react-pdf/renderer  
**Date Picker**: react-day-picker  
**Icons**: lucide-react  
**HTTP Client**: axios  
**Search**: fuse.js (client-side search)

---

## 🔒 Security & Authorization

**Authentication**: JWT tokens (2-hour expiry)  
**Authorization**: Role-based access control (RBAC) - Admin/Owner/Employee  
**Route Protection**: Client-side route guards + server-side API authorization  
**API Interceptor**: Axios interceptor adds JWT token to headers  
**Password**: Hashed in backend (Flask-JWT-Extended)

---

## 📱 Responsive Design

- **Tailwind CSS breakpoints**: Mobile-first design
- **Sidebar Navigation**: Collapsible on mobile
- **Data Tables**: Horizontal scroll on small screens
- **Forms**: Stack vertically on mobile
- **Charts**: Responsive canvas elements

---

## 🚀 Performance Optimization

- **Code Splitting**: Next.js automatic route-based splitting
- **Image Optimization**: Next.js Image component
- **API Caching**: Service layer caches queries
- **Lazy Loading**: Components lazy-loaded where needed
- **Pagination**: Large datasets paginated (20-50 items/page)
- **PDF Generation**: Client-side with @react-pdf/renderer

---

## 🔗 Navigation Structure

```
Login → {Role Selection}
    ↓
    ├─ Admin → Dashboard
    │   ├─ Users Management
    │   ├─ Subscriptions
    │   ├─ Payment Methods
    │   ├─ Analytics
    │   └─ Settings
    │
    ├─ Owner → Dashboard
    │   ├─ Household
    │   ├─ Invoices (CRUD)
    │   ├─ Payments
    │   ├─ Customers
    │   ├─ Inventory & Warehouses
    │   ├─ Accounting & Reports
    │   ├─ Employees
    │   ├─ Subscription Management
    │   └─ Settings
    │
    └─ Employee → Dashboard
        ├─ Invoices (Create/View)
        ├─ Customers (View)
        ├─ Debt Records (View)
        └─ Settings
```

---

## 📊 Data Models Overview

### Invoice
```typescript
{
  id, invoice_no, household_id, customer_id,
  date, due_date, items: [{product_id, quantity, unit_price}],
  subtotal, tax_amount, discount, total,
  status: "Draft|Issued|Paid|Overdue", 
  created_by, created_at, updated_at
}
```

### Payment
```typescript
{
  id, invoice_id, household_id,
  amount, method: "Cash|Bank|Check",
  payment_date, reference_no,
  status: "Pending|Confirmed|Failed",
  created_at
}
```

### Customer
```typescript
{
  id, household_id, name, phone, email,
  address, tax_id, credit_limit,
  total_purchases, outstanding_balance,
  status: "Active|Inactive",
  created_at
}
```

### Product
```typescript
{
  id, household_id, name, sku, category,
  unit_price, unit_id, warehouse_id,
  stock_quantity, reorder_level,
  tax_category, status: "Active|Discontinued"
}
```

---

## ✨ Special Features

### 🤖 AI-Powered Components
- **AI Invoice Input**: Suggestion for items based on history
- **Address Autocomplete**: Goong Maps integration for address lookup
- **AI Button**: Smart input helper for common fields

### 📄 PDF Export & Print
- Invoice templates (professional & retail)
- Receipt templates
- Report exports to Excel format
- Batch print support

### 📱 Responsive & Mobile-First
- Sidebar collapses on mobile
- Touch-friendly buttons & interactions
- Mobile-optimized forms & tables

### 🔔 Real-time Notifications
- Toast notifications for actions
- Email notifications (configured in BE)
- In-app notification center

---

**Last Updated**: February 2, 2026  
**Frontend Framework**: Next.js 15 + React 18 + TypeScript  
**Styling**: Tailwind CSS 3  
**State Management**: React Context API + Local Storage  
**Data Fetching**: Axios + React Query patterns
