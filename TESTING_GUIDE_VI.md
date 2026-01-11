# Hướng dẫn Kiểm thử (Testing Guide)

Ứng dụng hiện đã được tích hợp **Swagger UI**, giúp bạn dễ dàng kiểm thử các API mà không cần cài đặt thêm công cụ như Postman.

## 1. Chuẩn bị Database

Hiện tại ứng dụng đang báo lỗi kết nối Database (`OperationalError`). Bạn cần đảm bảo:
1.  Đã cài đặt **SQL Server** (hoặc chạy qua Docker).
2.  Đã tạo database tên là `PlatformDB` (theo file `config.py`).
3.  Cấu hình chuỗi kết nối trong file `.env` hoặc `src/config.py` đúng với môi trường của bạn.

**Cấu hình mặc định trong code:**
```python
# src/config.py
DATABASE_URI = 'mssql+pymssql://sa:%40Bina0608@127.0.0.1:1433/PlatformDB'
```

## 2. Khởi động Ứng dụng

Mở terminal tại thư mục gốc của dự án và chạy:

```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/src
python src/app.py
```

Nếu thành công, bạn sẽ thấy dòng:
`* Running on http://127.0.0.1:9999`

## 3. Truy cập Swagger UI

Mở trình duyệt và truy cập:
👉 **[http://localhost:9999/docs](http://localhost:9999/docs)**

Giao diện Swagger sẽ liệt kê tất cả các API endpoints.

## 4. Quy trình Test (Luồng cơ bản)

### Bước 1: Đăng nhập (Lấy Token)
1.  Tìm section **Auth** > `POST /api/auth/login`.
2.  Nhấn **Try it out**.
3.  Nhập JSON:
    ```json
    {
      "username": "your_username",
      "password": "your_password"
    }
    ```
4.  Nhấn **Execute**.
5.  Copy giá trị `token` trong kết quả trả về (`Response body`).

### Bước 2: Xác thực (Authorize)
1.  Kéo lên đầu trang Swagger, nhấn nút **Authorize** (ổ khóa 🔓).
2.  Nhập token vào ô **Value** (chỉ cần dán token, KHÔNG cần chữ `Bearer`).
3.  Nhấn **Authorize** > **Close**.
4.  Ổ khóa sẽ đóng lại 🔒, nghĩa là bạn đã đăng nhập thành công.

### Bước 3: Test các API khác
Ví dụ: Tạo hóa đơn nháp (Employee)
1.  Tìm section **Employee Invoice** > `POST /api/employee/invoices/`.
2.  Nhấn **Try it out**.
3.  Nhập dữ liệu hóa đơn mẫu.
4.  Nhấn **Execute** và kiểm tra kết quả.

## Ghi chú
- Nếu bạn gặp lỗi `500 Internal Server Error`, hãy kiểm tra lại kết nối Database.
- Nếu gặp lỗi `401 Unauthorized`, hãy kiểm tra lại Token (đã hết hạn hoặc chưa Authorize).
