Mục tiêu

- Sửa các lỗi cú pháp/merge trong mã nguồn, cho phép chạy ứng dụng cục bộ bằng SQLite khi `DATABASE_URI` không được cấu hình, và thêm các script seed để khởi tạo dữ liệu thử nghiệm (roles, admin, users, domain data).

Thay đổi chính

- Sửa file model/codemarked bị chèn Markdown: `src/infrastructure/models/product_model.py` (và các file tương tự nếu có).
- DB adapter: `src/infrastructure/databases/mssql.py` — xác thực/sanitize `DATABASE_URI`, fallback sang SQLite dev (`src/dev.db`), thêm `scoped_session`.
- Middleware / routes: `src/api/middleware.py`, `src/api/routes.py` — dọn lỗi và xử lý JWT/ghi log.
- Seed scripts: `src/seed_roles_and_functions.py`, `src/seed_admin_user.py`, `src/seed_sample_data.py`, `src/scripts/seed_domain_sample.py`.
- Helper test script: `src/scripts/fetch_endpoints.py` — script tự động đăng nhập và kiểm tra một số endpoint.
- Cập nhật `.gitignore` để bỏ qua `src/dev.db`.

Kiểm thử (tóm tắt)

1. Tạo virtualenv và cài dependencies:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r src/requirements.txt
```

2. Seed local DB (tuỳ chọn):

```powershell
$env:DATABASE_URI='sqlite:///src/dev.db'
python src/seed_roles_and_functions.py
python src/seed_admin_user.py
python src/seed_sample_data.py
python src/scripts/seed_domain_sample.py
```

3. Chạy server dùng DB dev:

```powershell
$env:DATABASE_URI='sqlite:///src/dev.db'
python src/app.py
```

4. Kiểm thử manual: POST `/api/auth/login` với `kc1015` / `58997` và kiểm tra các list endpoints.

Ghi chú

- Seeder có tính idempotent một phần; tránh chạy seed tạo trùng nhiều lần hoặc điều chỉnh script nếu cần re-seed sạch.
- Nếu muốn, có thể tách PR này thành hai PR nhỏ hơn: (1) dọn file/cấu hình, (2) seed & scripts.

