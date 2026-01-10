# Platform to Support Digital Transformation for Household Businesses

**Vietnamese:** Nền tảng hỗ trợ chuyển đổi số cho hộ kinh doanh.  
**Abbreviation:** BizFlow

## a. Context

*   **Economic Role:** In Vietnam, household businesses play a critical role in the local economy, especially in traditional sectors such as building materials, construction supplies, and hardware retail. The majority of these fall under Group 1 or Group 2 classifications as defined by the Ministry of Finance's Decision 3389/QĐ-BTC (2025).
*   **Current State:** Consequently, most of these businesses still operate using fully manual workflows. Daily tasks such as recording sales, managing inventory, tracking customer debts, and processing phone/Zalo orders are typically performed with handwritten notebooks or simple Excel files. Moreover, household businesses often lack the budget to hire accountants.
*   **Gap in Market:** Despite the rapidly growing demand for digital transformation across industries, existing commercial POS or business management solutions are often designed for restaurants, retail fashion, or large enterprises. These systems fail to meet the unique operational characteristics of household businesses, which include:
    *   Multi-channel orders (at-counter sales and phone/Zalo orders).
    *   Customer debt management with long-term transaction history.
    *   Low digital literacy among store owners.
*   **Hardware Limitations:** Most household businesses also lack the essential hardware required to adopt existing digital solutions. Many operate with only a single smartphone, without computers, barcode scanners, receipt printers, POS terminals, or cash drawers. This limitation makes POS systems impractical, as such solutions typically require multiple devices and a stable hardware setup. The high upfront cost of purchasing these devices further prevents household businesses from transitioning to digital workflows, forcing them to continue relying on fully manual processes.
*   **Challenges:** Due to the lack of a specialized platform, household businesses face several challenges: frequent errors in manual calculations, slow order processing, difficulty tracking inventory, inconsistent debt records, and no access to real-time business insights. The result is reduced operational efficiency, financial risks, and an inability to scale or modernize business operations.
*   **Proposed Solution:** To address this gap, we propose developing a **Platform to support digital transformation for household businesses**, a comprehensive system designed specifically for traditional stores. The platform integrates an interface with an AI-powered assistant capable of understanding natural language requests (via text or voice) to automatically create draft orders and auto fill data into templates. This combination supports automation, reduces human errors, and provides business owners with real-time visibility into their operations.

## b. Proposed Solutions

Build an application (mobile and/or web) that supports the following core functionalities:

### Roles & Responsibilities

#### Employee
*   Login to the system.
*   Create at-counter orders quickly (search products, add quantity, add customers details).
*   Print sales orders.
*   Record debt for registered customers.
*   Receive real-time notifications for new orders.
*   View and confirm "Draft Orders" created by the AI.

#### Owner
*   *Includes all Employee permissions.*
*   Manage product catalog (name, price, multiple units of measure).
*   Manage inventory (new stock, view stock levels).
*   Manage customers (info, purchase history, debt).
*   View reports and analytics (daily/monthly revenue, best-sellers, outstanding debt).
*   Manage employee accounts.

#### Administrator
*   Manage owner accounts.
*   View reports, analytics and feedback.
*   Manage Subscription Pricing.
*   Update system config and templates for financial reports.

#### System
*   Convert natural language into draft order.
*   Automatically does the bookkeeping.

---

### Functional Requirements

#### Employee
*   **Login:** Employees can log in using an account.
*   **Create At-Counter Orders:** Employees can quickly create orders for walk-in customers. They can search products, select quantity, assign customers (optional), and add items to the cart. The interface must support fast operations through keyboard shortcuts and instant product filtering.
*   **Record debt for registered customers:** If the customer chooses to buy on credit, the Employee can record the debt directly during order creation. The system automatically updates the customer’s outstanding balance.
*   **Print Sales Orders:** After creating an order, the employee can generate and print orders using pre-designed bill templates. The system stores each order in the database for future retrieval.
*   **Receive Real-Time Notifications for AI/Chatbot Orders:** When the AI assistant receives a message (text or voice) and generates a draft order, the interface will immediately display a real-time notification.
*   **View and confirm "Draft Orders" created by the AI:** The draft order will be sent to the employee for checking and confirmation.

#### Owner
*(Owner includes all Employee functions, plus the following additional capabilities)*
*   **Manage Product Catalog:** The owner can create, update, or disable products. They can define product attributes such as name, images, price, category, and multiple units of measure. Pricing rules can also be configured.
*   **Manage Inventory:** The owner can record stock imports, track stock levels in real time, and view inventory history. The system automatically deducts stock upon order confirmation.
*   **Manage Customers:** The owner can add and update customer information, view their purchase history, track outstanding debts, and review payment logs.
*   **View Reports & Analytics:** Provides interactive dashboards that show daily/weekly/monthly revenue, top-selling products, low-stock alerts, and total outstanding debts. Data visualization supports charts and summary widgets.
*   **Manage Employee Accounts:** The owner can create new employee accounts, reset passwords and deactivate accounts. Audit logs track who made each change for accountability.

#### System
*   **Convert natural language into draft order:** It "listens" (or reads) what the user says (e.g., "get 5 cement bags for Mr. Ba, put it on his tab") and automatically creates a draft order from that command.
*   **Automatically does the bookkeeping:** The system automatically performs bookkeeping for every sale, stock import, and customer debt transaction. Based on this recorded data, it automatically calculates, summarizes, and populates the official accounting books and financial reports required by **Circular 88/2021/TT-BTC** (Vietnam's official accounting standard for household businesses). This feature eliminates all manual calculation and data entry in Excel, ensuring that reports (e.g., Detailed Revenue Ledger, Outstanding Debt Report, Business Operations Report) are accurate and legally compliant for tax purposes. The platform guarantees that these report templates will be continuously updated to align with the latest government regulations as they are issued, ensuring long-term compliance for the business owner.

#### Administrator
*   **Owner Account Management:** Admins can view, search, filter, and manage all registered "Owner" (business household) accounts. This includes activating or deactivating accounts, and viewing detailed profiles.
*   **Manage Subscription Pricing:** Admins can define and update the pricing for the various subscription plans offered on the platform (e.g., set the monthly/annual cost for the Basic, Pro plans).
*   **Platform Analytics & Reporting:** Admins can access a global dashboard to monitor the health, growth, and revenue of the entire platform. This includes viewing total active users, new subscriptions.
*   **System & AI Configuration:** Admins can manage global system settings. Updating the master templates for financial reports (Circular 88/2021/TT-BTC), and broadcasting system-wide announcements.

### Non-functional Requirements

1.  **Security & Privacy**
    *   Protect the sales information of household businesses.
    *   Strict role-based access control for Employee, Owner, and Admin roles.
2.  **Performance & Scalability**
    *   Application responds quickly (< 2000 ms for core actions).
    *   Supports large product catalogs and multiple concurrent users.
3.  **Reliability & AI Accuracy**
    *   Employees or owners can review, edit, or reject AI-generated draft orders.
    *   Fall back to manual operation if AI is unavailable.
4.  **Usability & Accessibility**
    *   Simple, responsive web/mobile UI suitable for low digital literacy.
    *   Vietnamese interface; Unicode preserved.
    *   Real-time notifications.
5.  **Compliance & Reporting**
    *   Automatically generates accounting reports following Circular 88/2021/TT-BTC.
    *   Owners can review, edit, or reject AI-generated reports.
    *   The platform guarantees that all accounting report templates will be continuously updated to align with any future changes in the official declaration forms issued by the tax authorities.

---

## 3.2. Main Proposal Content (including result and product)

### a. Theory and Practice (Document)
*   Students should apply the software development process and UML 2.0 to model the system.
*   **The documentation includes:**
    *   User Requirement
    *   Software Requirement Specification
    *   Architecture Design
    *   Detailed Design
    *   System Implementation
    *   Testing Document
    *   Installation Guide
    *   Source code and deployable software packages
*   **Server-side technologies:**
    *   Clean architecture implemented in Python (BE)
    *   Data storage with SQL Server and PostgreSQL
    *   Caching: Redis
*   **AI:** Python
    *   RAG: ChromaDB, text-embedding-3-small
    *   LLM: OpenAI/Gemini
    *   Speech-to-Text: Google Speech-to-Text/Whisper
*   **Client-side technologies:**
    *   Mobile application: Flutter, Notification.
    *   Web Client: NextJS, Tanstack Query, Shadcn UI, TailwindCSS

### b. Products
*   Mobile application
*   Web application

### c. Proposed Tasks
*   **Task Package 1:** Deploy databases (MySQL and PostgreSQL)
*   **Task Package 2:** Set up clean architecture with Python
*   **Task Package 3:** Develop and deploy the mobile application using Flutter
*   **Task Package 4:** Develop and deploy the web application

## Appendix: Function Permissions

### 1. Admin (F0xx)
| Code | Name | Methods |
| :--- | :--- | :--- |
| F001 | manage_households | C,R,U,D |
| F002 | manage_subscription_plans | C,R,U,D |
| F003 | manage_subscriptions | C,R,U,D |
| F004 | view_platform_analytics | R |
| F005 | manage_admin_users | C,R,U,D |
| F006 | manage_system_config | R,U |
| F007 | view_all_accounting_ledgers | R |

### 2. Owner (F1xx)
| Code | Name | Methods |
| :--- | :--- | :--- |
| F101 | manage_employees | C,R,U,D |
| F102 | view_own_household | R,U |
| F103 | manage_categories | C,R,U,D |
| F104 | manage_products | C,R,U,D |
| F105 | manage_units | C,R,U,D |
| F106 | manage_inventory | C,R,U,D |
| F107 | manage_warehouses | C,R,U,D |
| F108 | manage_import_receipts | C,R,U,D |
| F109 | manage_customers | C,R,U,D |
| F110 | manage_sellers | C,R,U,D |
| F111 | manage_all_invoices | C,R,U,D |
| F112 | manage_payments | C,R,U,D |
| F113 | manage_payment_methods | C,R,U,D |
| F114 | manage_debt_records | C,R,U,D |
| F115 | view_household_reports | R |
| F116 | view_accounting_ledgers | R |
| F117 | export_reports | R |
| F118 | manage_export_receipts | C,R,U,D |

### 3. Employee (F2xx)
| Code | Name | Methods |
| :--- | :--- | :--- |
| F201 | view_products | R |
| F202 | view_categories | R |
| F203 | view_inventory | R |
| F204 | view_units | R |
| F205 | view_customers | R |
| F206 | view_customer_debt | R |
| F207 | create_sales_invoice | C,R |
| F208 | view_own_invoices | R |
| F209 | update_draft_invoice | U |
| F210 | confirm_invoice | U |
| F211 | record_payment | C,R |
| F212 | record_debt | C,R |
| F213 | view_draft_orders | R |
| F214 | confirm_draft_order | U |
| F215 | receive_notifications | R |
### Rules
1/ 25 model entities ở infrastructure là nền tảng không đụng vào, bám sát để code BE, yêu cầu đúng từng field và các quan hệ khóa chính khóa ngoại.
2/ Todo là code mẫu, là chuẩn mực của toàn bộ Flask clean architecture system, yêu cầu dựa vào để code.
3/ API ở phần Controller gọi Service, rồi từ Service gọi Repositories.
4/ API được gọi nhận JSON body, ở phần Domain thực hiện Object Data Transfer Object, tầng Service lấy Object DTO đó quăng xuống thằng Repositories thực hiện quá trình mapping từ Object DTO thành Object Model, rồi nó mới migrations xuống cơ sở dữ liệu.
5/ Luồng ngược lại khi call API, FE nhận Json body để thực hiện.
6/ Không tạo các file.md để tránh rối code.
7/ Đọc kĩ file documents.md là yêu cầu từ khách hàng, đối chiếu yêu cầu và 25 models để thực hiện đầy đủ
8/ Chưa đụng tới phần AI Draft Orders.

### Phân công
### **Phan Đức Lương: Authentication & Authorization**

**Models:** `User`, `Role`, `Function`, `RoleFunction`

**Files cần code:**

**Domain:**
- `src/domain/models/user.py`
- `src/domain/models/iuser_repository.py`
- `src/domain/models/role.py`
- `src/domain/models/irole_repository.py`
- `src/domain/models/function.py`
- `src/domain/models/ifunction_repository.py`
- `src/domain/models/role_function.py`
- `src/domain/models/irole_function_repository.py`

**Service:**
- `src/services/user_service.py`
- `src/services/role_service.py`
- `src/services/function_service.py`
- `src/services/role_function_service.py`

**Repository:**
- `src/infrastructure/repositories/user_repository.py`
- `src/infrastructure/repositories/role_repository.py`
- `src/infrastructure/repositories/function_repository.py`
- `src/infrastructure/repositories/role_function_repository.py`

**API:**
- `src/api/controllers/auth_controller.py` (login, logout, me)
- `src/api/controllers/user_controller.py` (CRUD users)
- `src/api/controllers/role_controller.py` (CRUD roles)
- `src/api/controllers/function_controller.py` (CRUD functions)
- `src/api/controllers/role_function_controller.py` (assign functions to roles)
- `src/api/schemas/user.py`
- `src/api/schemas/role.py`
- `src/api/schemas/function.py`
- `src/api/schemas/role_function.py`

**Routes:** Đăng ký trong `src/api/routes.py`

**ENDPOINTS CẦN CODE:**

**Auth Controller:**
- `POST /api/auth/login` - Login (All roles)
- `POST /api/auth/logout` - Logout (All roles)
- `GET /api/auth/me` - Get current user (All roles)

**User Controller (Admin - F005):**
- `GET /api/admin/users` - List all users (Admin only)
- `POST /api/admin/users` - Create user (Admin only)
- `GET /api/admin/users/<id>` - Get user by id (Admin only)
- `PUT /api/admin/users/<id>` - Update user (Admin only)
- `DELETE /api/admin/users/<id>` - Delete user (Admin only)

**User Controller (Owner - F101):**
- `GET /api/owner/employees` - List employees of household (Owner only)
- `POST /api/owner/employees` - Create employee (Owner only)
- `GET /api/owner/employees/<id>` - Get employee by id (Owner only)
- `PUT /api/owner/employees/<id>` - Update employee (Owner only)
- `DELETE /api/owner/employees/<id>` - Delete employee (Owner only)

**Role Controller (Admin only):**
- `GET /api/admin/roles` - List all roles (Admin only)
- `POST /api/admin/roles` - Create role (Admin only)
- `GET /api/admin/roles/<id>` - Get role by id (Admin only)
- `PUT /api/admin/roles/<id>` - Update role (Admin only)
- `DELETE /api/admin/roles/<id>` - Delete role (Admin only)

**Function Controller (Admin only):**
- `GET /api/admin/functions` - List all functions (Admin only)
- `POST /api/admin/functions` - Create function (Admin only)
- `GET /api/admin/functions/<id>` - Get function by id (Admin only)
- `PUT /api/admin/functions/<id>` - Update function (Admin only)
- `DELETE /api/admin/functions/<id>` - Delete function (Admin only)
**RoleFunction Controller (Admin only):**
- `GET /api/admin/roles/<role_id>/functions` - Get functions of role (Admin only)
- `POST /api/admin/roles/<role_id>/functions` - Assign function to role (Admin only)
- `DELETE /api/admin/roles/<role_id>/functions/<function_id>` - Remove function from role (Admin only)

---

### *Linh Đa*THÀNH VIÊN 2: Household & Subscription**

**Models:** `Household`, `Subscription`, `SubscriptionPlan`

**Files cần code:**

**Domain:**
- `src/domain/models/household.py`
- `src/domain/models/ihousehold_repository.py`
- `src/domain/models/subscription.py`
- `src/domain/models/isubscription_repository.py`
- `src/domain/models/subscription_plan.py`
- `src/domain/models/isubscription_plan_repository.py`

**Service:**
- `src/services/household_service.py`
- `src/services/subscription_service.py`
- `src/services/subscription_plan_service.py`

**Repository:**
- `src/infrastructure/repositories/household_repository.py`
- `src/infrastructure/repositories/subscription_repository.py`
- `src/infrastructure/repositories/subscription_plan_repository.py`

**API:**
- `src/api/controllers/household_controller.py`
- `src/api/controllers/subscription_controller.py`
- `src/api/controllers/subscription_plan_controller.py`
- `src/api/schemas/household.py`
- `src/api/schemas/subscription.py`
- `src/api/schemas/subscription_plan.py`

**Routes:** Đăng ký trong `src/api/routes.py`

**ENDPOINTS CẦN CODE:**

**Household Controller (Admin - F001):**
- `GET /api/admin/households` - List all households (Admin only)
- `POST /api/admin/households` - Create household (Admin only)
- `GET /api/admin/households/<id>` - Get household by id (Admin only)
- `PUT /api/admin/households/<id>` - Update household (Admin only)
- `DELETE /api/admin/households/<id>` - Delete household (Admin only)

**Household Controller (Owner - F102):**
- `GET /api/owner/household` - Get own household (Owner only)
- `PUT /api/owner/household` - Update own household (Owner only)

**SubscriptionPlan Controller (Admin - F002):**
- `GET /api/admin/subscription-plans` - List all subscription plans (Admin only)
- `POST /api/admin/subscription-plans` - Create subscription plan (Admin only)
- `GET /api/admin/subscription-plans/<id>` - Get subscription plan by id (Admin only)
- `PUT /api/admin/subscription-plans/<id>` - Update subscription plan (Admin only)
- `DELETE /api/admin/subscription-plans/<id>` - Delete subscription plan (Admin only)

**Subscription Controller (Admin - F003):**
- `GET /api/admin/subscriptions` - List all subscriptions (Admin only)
- `POST /api/admin/subscriptions` - Create subscription (Admin only)
- `GET /api/admin/subscriptions/<id>` - Get subscription by id (Admin only)
- `PUT /api/admin/subscriptions/<id>` - Update subscription (Admin only)
- `DELETE /api/admin/subscriptions/<id>` - Delete subscription (Admin only)

---

### **CẨM TÚ: THÀNH VIÊN 3: Product Management**

**Models:** `Product`, `Category`, `Unit`, `Warehouse`

**Files cần code:**

**Domain:**
- `src/domain/models/product.py`
- `src/domain/models/iproduct_repository.py`
- `src/domain/models/category.py`
- `src/domain/models/icategory_repository.py`
- `src/domain/models/unit.py`
- `src/domain/models/iunit_repository.py`
- `src/domain/models/warehouse.py`
- `src/domain/models/iwarehouse_repository.py`

**Service:**
- `src/services/product_service.py`
- `src/services/category_service.py`
- `src/services/unit_service.py`
- `src/services/warehouse_service.py`

**Repository:**
- `src/infrastructure/repositories/product_repository.py`
- `src/infrastructure/repositories/category_repository.py`
- `src/infrastructure/repositories/unit_repository.py`
- `src/infrastructure/repositories/warehouse_repository.py`

**API:**
- `src/api/controllers/product_controller.py`
- `src/api/controllers/category_controller.py`
- `src/api/controllers/unit_controller.py`
- `src/api/controllers/warehouse_controller.py`
- `src/api/schemas/product.py`
- `src/api/schemas/category.py`
- `src/api/schemas/unit.py`
- `src/api/schemas/warehouse.py`

**Routes:** Đăng ký trong `src/api/routes.py`

**ENDPOINTS CẦN CODE:**

**Product Controller (Owner - F104):**
- `GET /api/owner/products` - List products (Owner only)
- `POST /api/owner/products` - Create product (Owner only)
- `GET /api/owner/products/<id>` - Get product by id (Owner only)
- `PUT /api/owner/products/<id>` - Update product (Owner only)
- `DELETE /api/owner/products/<id>` - Delete product (Owner only)

**Product Controller (Employee - F201):**
- `GET /api/employee/products` - List products (Employee only, read-only)
- `GET /api/employee/products/<id>` - Get product by id (Employee only, read-only)

**Category Controller (Owner - F103):**
- `GET /api/owner/categories` - List categories (Owner only)
- `POST /api/owner/categories` - Create category (Owner only)
- `GET /api/owner/categories/<id>` - Get category by id (Owner only)
- `PUT /api/owner/categories/<id>` - Update category (Owner only)
- `DELETE /api/owner/categories/<id>` - Delete category (Owner only)

**Category Controller (Employee - F202):**
- `GET /api/employee/categories` - List categories (Employee only, read-only)

**Unit Controller (Owner - F105):**
- `GET /api/owner/units` - List units (Owner only)
- `POST /api/owner/units` - Create unit (Owner only)
- `GET /api/owner/units/<id>` - Get unit by id (Owner only)
- `PUT /api/owner/units/<id>` - Update unit (Owner only)
- `DELETE /api/owner/units/<id>` - Delete unit (Owner only)

**Unit Controller (Employee - F204):**
- `GET /api/employee/units` - List units (Employee only, read-only)

**Warehouse Controller (Owner - F107):**
- `GET /api/owner/warehouses` - List warehouses (Owner only)
- `POST /api/owner/warehouses` - Create warehouse (Owner only)
- `GET /api/owner/warehouses/<id>` - Get warehouse by id (Owner only)
- `PUT /api/owner/warehouses/<id>` - Update warehouse (Owner only)
- `DELETE /api/owner/warehouses/<id>` - Delete warehouse (Owner only)

---

###Kim Chi **THÀNH VIÊN 4: Customer & Seller**

**Models:** `Customer`, `Seller`

**Files cần code:**

**Domain:**
- `src/domain/models/customer.py`
- `src/domain/models/icustomer_repository.py`
- `src/domain/models/seller.py`
- `src/domain/models/iseller_repository.py`

**Service:**
- `src/services/customer_service.py`
- `src/services/seller_service.py`

**Repository:**
- `src/infrastructure/repositories/customer_repository.py`
- `src/infrastructure/repositories/seller_repository.py`

**API:**
- `src/api/controllers/customer_controller.py`
- `src/api/controllers/seller_controller.py`
- `src/api/schemas/customer.py`
- `src/api/schemas/seller.py`

**Routes:** Đăng ký trong `src/api/routes.py`

**ENDPOINTS CẦN CODE:**

**Customer Controller (Owner - F109):**
- `GET /api/owner/customers` - List customers (Owner only)
- `POST /api/owner/customers` - Create customer (Owner only)
- `GET /api/owner/customers/<id>` - Get customer by id (Owner only)
- `PUT /api/owner/customers/<id>` - Update customer (Owner only)
- `DELETE /api/owner/customers/<id>` - Delete customer (Owner only)
- `GET /api/owner/customers/<id>/history` - Get customer purchase history (Owner only)
- `GET /api/owner/customers/<id>/debt` - Get customer outstanding debt (Owner only)

**Customer Controller (Employee - F205, F206):**
- `GET /api/employee/customers` - List customers (Employee only, read-only)
- `GET /api/employee/customers/<id>` - Get customer by id (Employee only, read-only)
- `GET /api/employee/customers/<id>/debt` - Get customer debt (Employee only, read-only)

**Seller Controller (Owner - F110):**
- `GET /api/owner/sellers` - List sellers (Owner only)
- `POST /api/owner/sellers` - Create seller (Owner only)
- `GET /api/owner/sellers/<id>` - Get seller by id (Owner only)
- `PUT /api/owner/sellers/<id>` - Update seller (Owner only)
- `DELETE /api/owner/sellers/<id>` - Delete seller (Owner only)

---

###  ** TUẤN -THÀNH VIÊN 5: Invoice & Order**

**Models:** `Invoice`, `InvoiceDetail`

**Files cần code:**

**Domain:**
- `src/domain/models/invoice.py`
- `src/domain/models/iinvoice_repository.py`
- `src/domain/models/invoice_detail.py`
- `src/domain/models/iinvoice_detail_repository.py`

**Service:**
- `src/services/invoice_service.py`
- `src/services/invoice_detail_service.py`

**Repository:**
- `src/infrastructure/repositories/invoice_repository.py`
- `src/infrastructure/repositories/invoice_detail_repository.py`

**API:**
- `src/api/controllers/invoice_controller.py`
- `src/api/controllers/invoice_detail_controller.py`
- `src/api/schemas/invoice.py`
- `src/api/schemas/invoice_detail.py`

**Routes:** Đăng ký trong `src/api/routes.py`

**ENDPOINTS CẦN CODE:**

**Invoice Controller (Owner - F111):**
- `GET /api/owner/invoices` - List all invoices (Owner only)
- `POST /api/owner/invoices` - Create invoice (Owner only)
- `GET /api/owner/invoices/<id>` - Get invoice by id (Owner only)
- `PUT /api/owner/invoices/<id>` - Update invoice (Owner only)
- `DELETE /api/owner/invoices/<id>` - Delete invoice (Owner only)
- `GET /api/owner/invoices/<id>/details` - Get invoice details (Owner only)

**Invoice Controller (Employee - F207, F208, F209, F210):**
- `POST /api/employee/invoices` - Create draft invoice (Employee only)
- `GET /api/employee/invoices` - List own invoices (Employee only)
- `GET /api/employee/invoices/<id>` - Get invoice by id (Employee only)
- `PUT /api/employee/invoices/<id>` - Update draft invoice (Employee only)
- `PUT /api/employee/invoices/<id>/confirm` - Confirm invoice (Employee only)
- `GET /api/employee/invoices/<id>/details` - Get invoice details (Employee only)

**Draft Order Controller (Employee - F213, F214):**
- `GET /api/employee/draft-orders` - View draft orders from AI (Employee only)
- `PUT /api/employee/draft-orders/<id>/confirm` - Confirm draft order (Employee only)

**InvoiceDetail Controller:**
- `GET /api/invoices/<invoice_id>/details` - List invoice details (Owner/Employee)
- `POST /api/invoices/<invoice_id>/details` - Create invoice detail (Owner/Employee)
- `GET /api/invoices/<invoice_id>/details/<id>` - Get invoice detail by id (Owner/Employee)
- `PUT /api/invoices/<invoice_id>/details/<id>` - Update invoice detail (Owner/Employee)
- `DELETE /api/invoices/<invoice_id>/details/<id>` - Delete invoice detail (Owner/Employee)

---

### **THÀNH VIÊN 6: Import/Export & Inventory**

**Models:** `ImportReceipt`, `ImportDetail`, `ExportReceipt`, `ExportDetail`, `Inventory`

**Files cần code:**

**Domain:**
- `src/domain/models/import_receipt.py`
- `src/domain/models/iimport_receipt_repository.py`
- `src/domain/models/import_detail.py`
- `src/domain/models/iimport_detail_repository.py`
- `src/domain/models/export_receipt.py`
- `src/domain/models/iexport_receipt_repository.py`
- `src/domain/models/export_detail.py`
- `src/domain/models/iexport_detail_repository.py`
- `src/domain/models/inventory.py`
- `src/domain/models/iinventory_repository.py`

**Service:**
- `src/services/import_receipt_service.py`
- `src/services/import_detail_service.py`
- `src/services/export_receipt_service.py`
- `src/services/export_detail_service.py`
- `src/services/inventory_service.py`

**Repository:**
- `src/infrastructure/repositories/import_receipt_repository.py`
- `src/infrastructure/repositories/import_detail_repository.py`
- `src/infrastructure/repositories/export_receipt_repository.py`
- `src/infrastructure/repositories/export_detail_repository.py`
- `src/infrastructure/repositories/inventory_repository.py`

**API:**
- `src/api/controllers/import_receipt_controller.py`
- `src/api/controllers/import_detail_controller.py`
- `src/api/controllers/export_receipt_controller.py`
- `src/api/controllers/export_detail_controller.py`
- `src/api/controllers/inventory_controller.py`
- `src/api/schemas/import_receipt.py`
- `src/api/schemas/import_detail.py`
- `src/api/schemas/export_receipt.py`
- `src/api/schemas/export_detail.py`
- `src/api/schemas/inventory.py`

**Routes:** Đăng ký trong `src/api/routes.py`

**ENDPOINTS CẦN CODE:**

**ImportReceipt Controller (Owner - F108):**
- `GET /api/owner/import-receipts` - List import receipts (Owner only)
- `POST /api/owner/import-receipts` - Create import receipt (Owner only)
- `GET /api/owner/import-receipts/<id>` - Get import receipt by id (Owner only)
- `PUT /api/owner/import-receipts/<id>` - Update import receipt (Owner only)
- `DELETE /api/owner/import-receipts/<id>` - Delete import receipt (Owner only)
- `PUT /api/owner/import-receipts/<id>/confirm` - Confirm import (tăng inventory) (Owner only)
- `GET /api/owner/import-receipts/<id>/details` - Get import receipt details (Owner only)

**ImportDetail Controller:**
- `GET /api/import-receipts/<receipt_id>/details` - List import details (Owner only)
- `POST /api/import-receipts/<receipt_id>/details` - Create import detail (Owner only)
- `GET /api/import-receipts/<receipt_id>/details/<id>` - Get import detail by id (Owner only)
- `PUT /api/import-receipts/<receipt_id>/details/<id>` - Update import detail (Owner only)
- `DELETE /api/import-receipts/<receipt_id>/details/<id>` - Delete import detail (Owner only)

**ExportReceipt Controller (Owner - F118):**
- `GET /api/owner/export-receipts` - List export receipts (Owner only)
- `POST /api/owner/export-receipts` - Create export receipt (Owner only)
- `GET /api/owner/export-receipts/<id>` - Get export receipt by id (Owner only)
- `PUT /api/owner/export-receipts/<id>` - Update export receipt (Owner only)
- `DELETE /api/owner/export-receipts/<id>` - Delete export receipt (Owner only)
- `PUT /api/owner/export-receipts/<id>/confirm` - Confirm export (giảm inventory) (Owner only)
- `GET /api/owner/export-receipts/<id>/details` - Get export receipt details (Owner only)

**ExportDetail Controller:**
- `GET /api/export-receipts/<receipt_id>/details` - List export details (Owner only)
- `POST /api/export-receipts/<receipt_id>/details` - Create export detail (Owner only)
- `GET /api/export-receipts/<receipt_id>/details/<id>` - Get export detail by id (Owner only)
- `PUT /api/export-receipts/<receipt_id>/details/<id>` - Update export detail (Owner only)
- `DELETE /api/export-receipts/<receipt_id>/details/<id>` - Delete export detail (Owner only)

**Inventory Controller (Owner - F106):**
- `GET /api/owner/inventory` - List inventory (Owner only)
- `POST /api/owner/inventory` - Create inventory record (Owner only)
- `GET /api/owner/inventory/<product_id>/<warehouse_id>` - Get inventory by product and warehouse (Owner only)
- `PUT /api/owner/inventory/<id>` - Update inventory (Owner only)
- `DELETE /api/owner/inventory/<id>` - Delete inventory (Owner only)

**Inventory Controller (Employee - F203):**
- `GET /api/employee/inventory` - List inventory (Employee only, read-only)
- `GET /api/employee/inventory/<product_id>/<warehouse_id>` - Get inventory by product and warehouse (Employee only, read-only)

---

### **THÀNH VIÊN 7: Payment & Accounting**

**Models:** `Payment`, `PaymentMethod`, `DebtRecord`, `AccountingLedger`

**Files cần code:**

**Domain:**
- `src/domain/models/payment.py`
- `src/domain/models/ipayment_repository.py`
- `src/domain/models/payment_method.py`
- `src/domain/models/ipayment_method_repository.py`
- `src/domain/models/debt_record.py`
- `src/domain/models/idebt_record_repository.py`
- `src/domain/models/accounting_ledger.py`
- `src/domain/models/iaccounting_ledger_repository.py`

**Service:**
- `src/services/payment_service.py`
- `src/services/payment_method_service.py`
- `src/services/debt_record_service.py`
- `src/services/accounting_ledger_service.py`

**Repository:**
- `src/infrastructure/repositories/payment_repository.py`
- `src/infrastructure/repositories/payment_method_repository.py`
- `src/infrastructure/repositories/debt_record_repository.py`
- `src/infrastructure/repositories/accounting_ledger_repository.py`

**API:**
- `src/api/controllers/payment_controller.py`
- `src/api/controllers/payment_method_controller.py`
- `src/api/controllers/debt_record_controller.py`
- `src/api/controllers/accounting_ledger_controller.py`
- `src/api/schemas/payment.py`
- `src/api/schemas/payment_method.py`
- `src/api/schemas/debt_record.py`
- `src/api/schemas/accounting_ledger.py`

**Routes:** Đăng ký trong `src/api/routes.py`

**ENDPOINTS CẦN CODE:**

**Payment Controller (Owner - F112):**
- `GET /api/owner/payments` - List payments (Owner only)
- `POST /api/owner/payments` - Create payment (Owner only)
- `GET /api/owner/payments/<id>` - Get payment by id (Owner only)
- `PUT /api/owner/payments/<id>` - Update payment (Owner only)
- `DELETE /api/owner/payments/<id>` - Delete payment (Owner only)

**Payment Controller (Employee - F211):**
- `POST /api/employee/payments` - Record payment (Employee only)
- `GET /api/employee/payments/<id>` - Get payment by id (Employee only)

**PaymentMethod Controller (Owner - F113):**
- `GET /api/owner/payment-methods` - List payment methods (Owner only)
- `POST /api/owner/payment-methods` - Create payment method (Owner only)
- `GET /api/owner/payment-methods/<id>` - Get payment method by id (Owner only)
- `PUT /api/owner/payment-methods/<id>` - Update payment method (Owner only)
- `DELETE /api/owner/payment-methods/<id>` - Delete payment method (Owner only)

**DebtRecord Controller (Owner - F114):**
- `GET /api/owner/debt-records` - List debt records (Owner only)
- `POST /api/owner/debt-records` - Create debt record (Owner only)
- `GET /api/owner/debt-records/<id>` - Get debt record by id (Owner only)
- `PUT /api/owner/debt-records/<id>` - Update debt record (Owner only)
- `DELETE /api/owner/debt-records/<id>` - Delete debt record (Owner only)

**DebtRecord Controller (Employee - F212):**
- `POST /api/employee/debt-records` - Record debt (Employee only)
- `GET /api/employee/debt-records/<id>` - Get debt record by id (Employee only)

**AccountingLedger Controller (Owner - F116, F117):**
- `GET /api/owner/accounting-ledgers` - List accounting ledgers (Owner only)
- `GET /api/owner/accounting-ledgers/export` - Export reports (Excel) (Owner only)
  - Query params: `format=excel&from_date=...&to_date=...`
- `GET /api/owner/reports/daily-revenue` - Daily revenue report (Owner only)
  - Query params: `date=...`
- `GET /api/owner/reports/monthly-revenue` - Monthly revenue report (Owner only)
  - Query params: `month=...&year=...`
- `GET /api/owner/reports/outstanding-debt` - Outstanding debt report (Owner only)

**AccountingLedger Controller (Admin - F007):**
- `GET /api/admin/accounting-ledgers` - List all accounting ledgers (Admin only)
- `GET /api/admin/accounting-ledgers/export` - Export all ledgers (Admin only)
  - Query params: `format=excel&household_id=...&from_date=...&to_date=...`

---

## Notes - Functions chưa phân công (làm sau):

- **F004** - view_platform_analytics (Admin) - Platform analytics dashboard
- **F006** - manage_system_config (Admin) - System configuration management
- **F115** - view_household_reports (Owner) - Household reports
- **F215** - receive_notifications (Employee) - Real-time notifications

## Seed Data Test
    cd src
    
    python scripts/seed_auth_data.py