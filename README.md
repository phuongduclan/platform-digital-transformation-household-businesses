# Architecture

```bash
    ├── migrations
    ├── scripts
    │   └── run_postgres.sh
    ├── src
    │   ├── api
    │   │   ├── controllers
    │   │   │   └── ...  # controllers for the api
    │   │   ├── schemas
    │   │   │   └── ...  # Marshmallow schemas
    │   │   ├── middleware.py
    │   │   ├── responses.py
    │   │   └── requests.py
    │   ├── infrastructure
    │   │   ├── services
    │   │   │   └── ...  # Services that use third party libraries or services (e.g. email service)
    │   │   ├── databases
    │   │   │   └── ...  # Database adapaters and initialization
    │   │   ├── repositories
    │   │   │   └── ...  # Repositories for interacting with the databases
    │   │   └── models
    │   │   │   └── ...  # Database models
    │   ├── domain
    │   │   ├── constants.py
    │   │   ├── exceptions.py
    │   │   ├── models
    │   │   │   └── ...  # Business logic models
    │   ├── services
    │   │    └── ...  # Services for interacting with the domain (business logic)
    │   ├── app.py
    │   ├── config.py
    │   ├── cors.py
    │   ├── create_app.py
    │   ├── dependency_container.py
    │   ├── error_handler.py
    │   └── logging.py
```

## Domain Layer

## Services Layer

## Infrastructure Layer

## Download source code (CMD)
    git clone https://github.com/phuongduclan/platform-digital-transformation-household-businesses.git
## Kiểm tra đã cài python đã cài đặt trên máy chưa
    python --version
## Run app

 - Bước 1: Tạo môi trường ảo co Python (phiên bản 3.x)
     ## Windows:
     		py -m venv .venv
     ## Unix/MacOS:
     		python3 -m venv .venv
   - Bước 2: Kích hoạt môi trường:
     ## Windows:
     		.venv\Scripts\activate.ps1
     ### Nếu xảy ra lỗi active .venv trên winos run powshell -->Administrator
         Set-ExecutionPolicy RemoteSigned -Force
     ## Unix/MacOS:
     		source .venv/bin/activate
     
   - Bước 3: Cài đặt các thư viện cần thiết
     ## Install:
     		pip install -r src/requirements.txt
   - Bước 4: Tạo file .env
     ## Tạo file .env ở root directory (cùng cấp với src/):
     	Tạo file `.env` với nội dung:
     	```
     	# Flask settings
     	FLASK_ENV=development
     	SECRET_KEY=a_default_secret_key
     	
     	# PostgreSQL Database Configuration (Supabase)
     	DATABASE_URI=postgresql://postgres.xjghpmiupxldgezcrucj:079206043460@aws-1-ap-southeast-2.pooler.supabase.com:5432/postgres
     	```
   - Bước 5: Chạy mã xử lý dữ liệu
     ## Run:
    	python app.py 
        

     Truy câp http://localhost:6868/docs

## ORM Flask (from sqlalchemy.orm )
Object Relational Mapping

Ánh xạ 1 class (OOP)  model src/infrastructure/models --> Table in database 
Ánh xạ các mối quan hệ (Relational) -- Khoá ngoại CSDL 
(n-n): many to many 