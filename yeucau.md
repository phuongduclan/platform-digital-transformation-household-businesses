# Module: Quản lý Hóa đơn & Đơn hàng (Invoice & Order)
**Vai trò: Thành viên 5**

Dưới đây là đặc tả kỹ thuật và danh sách các endpoint tập trung hoàn toàn vào luồng nghiệp vụ của Chủ hộ (Owner) và Nhân viên (Employee), không bao gồm các chức năng quản trị hệ thống (Admin).

## 1. Cấu trúc Mô hình (Models)
- **Invoice**: Quản lý thông tin chung của hóa đơn (Số hóa đơn, Tên khách hàng, Tổng tiền, Trạng thái, Nguồn gốc).
- **InvoiceDetail**: Chi tiết các mục trong hóa đơn (Tên sản phẩm, Số lượng, Đơn giá, Thành tiền).

## 2. Danh sách Endpoint

### A. Nghiệp vụ Chủ hộ (Owner - Quyền quản lý toàn diện)
Dành cho các chức năng kiểm soát và tra cứu hóa đơn của toàn bộ hộ kinh doanh.
- `GET /api/owner/invoices` - Danh sách toàn bộ hóa đơn của hộ kinh doanh.
- `POST /api/owner/invoices` - Tạo mới hóa đơn trực tiếp (Trạng thái mặc định: DRAFT/CONFIRMED).
- `GET /api/owner/invoices/<id>` - Xem chi tiết thông tin chung của một hóa đơn.
- `PUT /api/owner/invoices/<id>` - Cập nhật thông tin hóa đơn (Chỉ áp dụng cho trạng thái DRAFT).
- `DELETE /api/owner/invoices/<id>` - Xóa hóa đơn (Chỉ áp dụng cho hóa đơn nháp).
- `GET /api/owner/invoices/<id>/details` - Xem hóa đơn cùng toàn bộ danh sách sản phẩm đi kèm.

### B. Nghiệp vụ Nhân viên (Employee - Quyền tạo & Xác nhận)
Dành cho nhân viên bán hàng tại quầy hoặc xử lý đơn hàng từ AI.
- `POST /api/employee/invoices` - Tạo hóa đơn nháp (Trạng thái luôn là DRAFT).
- `GET /api/employee/invoices` - Danh sách các hóa đơn do chính nhân viên đó tạo ra.
- `GET /api/employee/invoices/<id>` - Xem chi tiết hóa đơn nháp của bản thân.
- `PUT /api/employee/invoices/<id>` - Chỉnh sửa hóa đơn nháp trước khi chốt.
- `PUT /api/employee/invoices/<id>/confirm` - Xác nhận hóa đơn nháp thành hóa đơn chính thức.
- `GET /api/employee/invoices/<id>/details` - Xem chi tiết sản phẩm trong hóa đơn của mình.

### C. Quản lý Đơn hàng từ AI (Draft Orders)
Xử lý các đơn hàng được hệ thống AI tự động gợi ý.
- `GET /api/employee/draft-orders` - Danh sách các đơn hàng chờ xử lý từ AI (Source: AI).
- `PUT /api/employee/draft-orders/<id>/confirm` - Kiểm tra và chuyển đổi đơn hàng AI thành hóa đơn thật.

### D. Chi tiết Hóa đơn (Common Invoice Details)
Các thao tác quản lý danh mục sản phẩm trong một hóa đơn.
- `GET /api/invoices/<invoice_id>/details` - Liệt kê sản phẩm trong hóa đơn.
- `POST /api/invoices/<invoice_id>/details` - Thêm sản phẩm vào hóa đơn.
- `GET /api/invoices/<invoice_id>/details/<id>` - Xem thông tin một dòng sản phẩm cụ thể.
- `PUT /api/invoices/<invoice_id>/details/<id>` - Cập nhật số lượng/đơn giá sản phẩm.
- `DELETE /api/invoices/<invoice_id>/details/<id>` - Xóa sản phẩm khỏi hóa đơn.

## 3. Quy tắc Kỹ thuật (Technical Rules)
1. **Security**: Mọi API yêu cầu Token hợp lệ (JWT).
2. **Architecture**: Tuân thủ Clean Architecture (Domain -> Service -> Repository).
3. **Validation**: Kiểm tra tính hợp lệ của dữ liệu (Số lượng > 0, Đơn giá >= 0) bằng Marshmallow.
4. **Logic**: `subtotal` của từng dòng và `total_amount` của hóa đơn phải được tự động tính toán/cập nhật.

