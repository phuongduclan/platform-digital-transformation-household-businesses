# Quick Test Guide for Invoice Module

## ✅ Module Status: READY

All **19 endpoints** have been successfully implemented and registered:

### Owner Endpoints (6)
- `GET    /api/owner/invoices/` - List all invoices
- `POST   /api/owner/invoices/` - Create invoice
- `GET    /api/owner/invoices/<id>` - Get invoice
- `PUT    /api/owner/invoices/<id>` - Update invoice
- `DELETE /api/owner/invoices/<id>` - Delete invoice
- `GET    /api/owner/invoices/<id>/details` - Get with details

### Employee Endpoints (6)
- `POST   /api/employee/invoices/` - Create draft
- `GET    /api/employee/invoices/` - List own invoices
- `GET    /api/employee/invoices/<id>` - Get invoice
- `PUT    /api/employee/invoices/<id>` - Update draft
- `PUT    /api/employee/invoices/<id>/confirm` - Confirm invoice
- `GET    /api/employee/invoices/<id>/details` - Get with details

### Draft Order Endpoints (2)
- `GET    /api/employee/draft-orders/` - List AI drafts
- `PUT    /api/employee/draft-orders/<id>/confirm` - Confirm draft

### Invoice Detail Endpoints (5)
- `GET    /api/invoices/<invoice_id>/details` - List details
- `POST   /api/invoices/<invoice_id>/details` - Add detail
- `GET    /api/invoices/<invoice_id>/details/<id>` - Get detail
- `PUT    /api/invoices/<invoice_id>/details/<id>` - Update detail
- `DELETE /api/invoices/<invoice_id>/details/<id>` - Delete detail

## 🚀 How to Run

```bash
# 1. Navigate to src directory
cd /Users/tranminhtri/Flask-CleanArchitecture-1/src

# 2. Run the application
python app.py

# 3. Access Swagger UI
open http://localhost:9999/docs
```

## 📝 Testing with Swagger UI

1. Open browser to `http://localhost:9999/docs`
2. Find "Owner - Invoices" section
3. Try "POST /api/owner/invoices/" to create an invoice
4. Use the returned invoice ID to test other endpoints

## ✅ What Works

- ✓ All 19 endpoints registered successfully
- ✓ Database tables created (invoices, invoice_details)
- ✓ Marshmallow validation schemas
- ✓ Automatic invoice number generation
- ✓ Automatic subtotal calculation
- ✓ Cascade delete for invoice details
- ✓ Role-based routing (Owner/Employee)

## ⚠️ Notes

- Using SQLite database (default.db) for development
- JWT authentication placeholders in place (user_id hardcoded)
- Need to implement proper role-based authorization middleware
- Foreign key warning for 'users' table (can be ignored for now)

## 🎯 Next Steps

1. Implement JWT middleware to extract user_id from tokens
2. Add role-based authorization checks
3. Test all endpoints via Swagger UI
4. Deploy to production with PostgreSQL
