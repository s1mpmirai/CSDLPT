# Flask Backend - Hệ thống Quản lý Lương & Hồ sơ Nhân sự

## Cấu trúc Project

```
backend/
├── app/
│   ├── models/
│   │   ├── nhanvien.py      # Models: NhanVien, PhongBan, ChucVu
│   │   └── luong.py         # Models: BangLuong, ChiTietLuongThang
│   ├── routes/
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── nhanvien.py      # Nhân viên endpoints
│   │   ├── luong.py         # Lương endpoints
│   │   ├── phongban.py      # Phòng ban endpoints
│   │   └── chucvu.py        # Chức vụ endpoints
│   ├── schemas/             # Marshmallow schemas (tùy chọn)
│   └── __init__.py          # Application factory
├── config.py                # Configuration
├── wsgi.py                  # Entry point
├── requirements.txt         # Dependencies
├── .env.example             # Environment variables template
└── README.md                # Documentation
```

## Setup & Installation

### 1. Cài đặt Python Dependencies

```bash
# Tạo virtual environment
python -m venv venv

# Activate virtual environment
# Trên Windows:
venv\Scripts\activate
# Trên macOS/Linux:
source venv/bin/activate

# Cài đặt dependencies
pip install -r requirements.txt
```

### 2. Cấu hình MySQL

Đảm bảo MySQL Server chạy và 2 database đã được tạo:
- DB1_NHANSU
- DB2_LUONG

Tạo user cho ứng dụng:
```sql
CREATE USER 'app_user'@'localhost' IDENTIFIED BY 'app_secure_password_123';
GRANT ALL PRIVILEGES ON DB1_NHANSU.* TO 'app_user'@'localhost';
GRANT ALL PRIVILEGES ON DB2_LUONG.* TO 'app_user'@'localhost';
FLUSH PRIVILEGES;
```

### 3. Cấu hình Environment Variables

```bash
# Copy .env.example to .env
cp .env.example .env

# Edit .env với thông tin của bạn
FLASK_ENV=development
FLASK_APP=wsgi.py
SECRET_KEY=your_secret_key_here
JWT_SECRET_KEY=your_jwt_secret_key_here
DATABASE_URL_DB1=mysql+pymysql://app_user:app_secure_password_123@localhost/DB1_NHANSU
DATABASE_URL_DB2=mysql+pymysql://app_user:app_secure_password_123@localhost/DB2_LUONG
```

### 4. Chạy Flask Server

```bash
# Cách 1: Dùng Flask CLI
flask run

# Cách 2: Dùng Python
python wsgi.py

# Cách 3: Dùng Gunicorn (Production)
pip install gunicorn
gunicorn wsgi:app
```

Server sẽ chạy tại: **http://localhost:5000**

---

## API Endpoints

### Authentication

#### Login
```
POST /api/auth/login
Content-Type: application/json

{
  "username": "admin",  // "admin", "ketoan", "nhanvien"
  "password": "admin123"
}

Response:
{
  "success": true,
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "username": "admin",
    "name": "Admin User",
    "role": "admin"
  }
}
```

#### Get User Info
```
GET /api/auth/me
Authorization: Bearer {token}

Response:
{
  "success": true,
  "user": {
    "username": "admin",
    "role": "admin"
  }
}
```

#### Logout
```
POST /api/auth/logout
Authorization: Bearer {token}

Response:
{
  "success": true,
  "message": "Logged out successfully"
}
```

---

### Nhân viên

#### Lấy danh sách nhân viên
```
GET /api/nhanvien?page=1&limit=20&phongBan=1&trangThai=1
Authorization: Bearer {token}

Response:
{
  "success": true,
  "data": [
    {
      "maNV": 1,
      "tenNV": "Nguyễn Văn A",
      "email": "nguyenvana@company.com",
      "tenPhong": "Kỹ Thuật",
      "tenChucVu": "Nhân viên",
      ...
    }
  ],
  "total": 50,
  "page": 1,
  "pages": 3
}
```

#### Lấy chi tiết nhân viên
```
GET /api/nhanvien/1
Authorization: Bearer {token}

Response:
{
  "success": true,
  "data": {
    "maNV": 1,
    "tenNV": "Nguyễn Văn A",
    ...
  }
}
```

#### Thêm nhân viên
```
POST /api/nhanvien
Authorization: Bearer {token}
Content-Type: application/json

{
  "tenNV": "Tô Thị I",
  "ngaySinh": "1998-09-12",
  "gioiTinh": "Nữ",
  "diaChi": "111 Đường...",
  "sdt": "0989012345",
  "email": "thothi@company.com",
  "maPhong": 1,
  "maChucVu": 3,
  "ngayVaoLam": "2024-01-01"
}

Response:
{
  "success": true,
  "message": "Thêm nhân viên thành công",
  "data": {...}
}
```

#### Cập nhật nhân viên
```
PUT /api/nhanvien/1
Authorization: Bearer {token}
Content-Type: application/json

{
  "tenNV": "Nguyễn Văn A Updated",
  "trangThai": 1
}

Response:
{
  "success": true,
  "message": "Cập nhật nhân viên thành công",
  "data": {...}
}
```

#### Xóa nhân viên
```
DELETE /api/nhanvien/1
Authorization: Bearer {token}

Response:
{
  "success": true,
  "message": "Xóa nhân viên thành công"
}
```

---

### Lương

#### Lấy bảng lương
```
GET /api/luong/1
Authorization: Bearer {token}

Response:
{
  "success": true,
  "data": {
    "maNV": 1,
    "luongCoBan": 5000000,
    "heSoLuong": 1.0,
    "phuCapChucVu": 500000,
    ...
  }
}
```

#### Cập nhật bảng lương
```
PUT /api/luong/1
Authorization: Bearer {token}
Content-Type: application/json

{
  "luongCoBan": 5500000,
  "heSoLuong": 1.05,
  "ngayApDung": "2024-03-01"
}

Response:
{
  "success": true,
  "message": "Cập nhật bảng lương thành công",
  "data": {...}
}
```

#### Tính lương tháng
```
POST /api/luong/chi-tiet
Authorization: Bearer {token}
Content-Type: application/json

{
  "thang": 3,
  "nam": 2026,
  "maNV": 1  // Optional - nếu không có sẽ tính cho tất cả
}

Response:
{
  "success": true,
  "message": "Tính lương thành công"
}
```

#### Lấy chi tiết lương tháng
```
GET /api/luong/chi-tiet/1?thang=3&nam=2026
Authorization: Bearer {token}

Response:
{
  "success": true,
  "data": {
    "maNV": 1,
    "thang": 3,
    "nam": 2026,
    "luongThucLinh": 6300000,
    ...
  }
}
```

#### Lấy danh sách lương tháng
```
GET /api/luong/danh-sach?thang=3&nam=2026
Authorization: Bearer {token}

Response:
{
  "success": true,
  "data": [
    {
      "maNV": 1,
      "tenNV": "Nguyễn Văn A",
      "luongThucLinh": 6300000,
      ...
    }
  ]
}
```

---

### Phòng ban

#### Lấy danh sách phòng ban
```
GET /api/phongban
Authorization: Bearer {token}

Response:
{
  "success": true,
  "data": [
    {
      "maPhong": 1,
      "tenPhong": "Kỹ Thuật",
      "truongPhong": "Nguyễn Văn A"
    }
  ]
}
```

#### Thêm phòng ban
```
POST /api/phongban
Authorization: Bearer {token}
Content-Type: application/json

{
  "tenPhong": "IT Support",
  "truongPhong": "Lê Văn C"
}

Response:
{
  "success": true,
  "message": "Thêm phòng ban thành công",
  "data": {...}
}
```

---

### Chức vụ

#### Lấy danh sách chức vụ
```
GET /api/chucvu
Authorization: Bearer {token}

Response:
{
  "success": true,
  "data": [
    {
      "maChucVu": 1,
      "tenChucVu": "Giám đốc"
    }
  ]
}
```

#### Thêm chức vụ
```
POST /api/chucvu
Authorization: Bearer {token}
Content-Type: application/json

{
  "tenChucVu": "Quản lý dự án"
}

Response:
{
  "success": true,
  "message": "Thêm chức vụ thành công",
  "data": {...}
}
```

---

## Test Credentials

```
Admin:
  username: admin
  password: admin123
  role: admin

Kế toán:
  username: ketoan
  password: ketoan123
  role: ketoan

Nhân viên:
  username: nhanvien
  password: nhanvien123
  role: nhanvien
```

---

## Phân quyền

| Endpoint | Admin | Kế toán | Nhân viên |
|----------|-------|---------|----------|
| GET /api/nhanvien | ✅ | ✅ | ❌ |
| POST /api/nhanvien | ✅ | ❌ | ❌ |
| PUT /api/nhanvien | ✅ | ❌ | ❌ |
| DELETE /api/nhanvien | ✅ | ❌ | ❌ |
| GET /api/luong | ✅ | ✅ | ✅ (riêng) |
| PUT /api/luong | ✅ | ✅ | ❌ |
| POST /api/luong/chi-tiet | ✅ | ✅ | ❌ |

---

## Troubleshooting

### Error: "No module named 'app'"
- Đảm bảo bạn ở trong thư mục `backend/`
- Chạy lại: `pip install -r requirements.txt`

### Error: "Can't connect to MySQL"
- Kiểm tra MySQL Server đang chạy
- Kiểm tra credentials trong `.env`
- Kiểm tra 2 database đã được tạo

### Error: "ModuleNotFoundError: No module named 'flask'"
- Activate virtual environment trước
- Chạy: `pip install -r requirements.txt`

---

## Development & Debugging

### Bật debug mode
```python
# In wsgi.py hoặc config.py
app.run(debug=True)
```

### View SQL queries
```python
# In config.py
SQLALCHEMY_ECHO = True
```

### Test API bằng curl
```bash
# Login
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Get nhân viên
curl -X GET http://localhost:5000/api/nhanvien \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## Next Steps

1. Tạo Frontend (React, Vue hoặc Django Templates)
2. Deploy lên production
3. Thêm logging & monitoring
4. Tối ưu performance (caching, indexing)
