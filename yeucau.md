### Minh Trí  
**  -THÀNH VIÊN 5: Invoice & Order**

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

