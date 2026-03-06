# 🚀 Hướng dẫn Setup cho Team

## Các bước setup để member khác chạy được project

### 1️⃣ **Clone Repository**
```bash
git clone <repository_url>
cd CSDLPT
```

---

### 2️⃣ **Setup Python Environment**

#### Windows:
```bash
# Tạo virtual environment
python -m venv myENV

# Activate
myENV\Scripts\activate

# Verify activation (terminal sẽ hiển thị (myENV) ở đầu)
```

#### macOS/Linux:
```bash
# Tạo virtual environment
python3 -m venv myENV

# Activate
source myENV/bin/activate

# Verify
```

---

### 3️⃣ **Install Dependencies**

```bash
cd backend

# Cài đặt tất cả packages
pip install -r requirements.txt
```

**Packages bắt buộc:**
- Flask 2.3.3
- Flask-SQLAlchemy 3.0.3
- Flask-Cors 4.0.0
- Flask-JWT-Extended 4.4.4
- PyMySQL 1.1.0
- python-dotenv 1.0.0

---

### 4️⃣ **Setup MySQL Database**

#### A. Tạo MySQL User (nếu chưa có)

```sql
-- Mở MySQL Command Line hoặc MySQL Workbench
-- Login với root account

-- Tạo user
CREATE USER 'app_user'@'localhost' IDENTIFIED BY 'app_secure_password_123';

-- Cấp quyền
GRANT ALL PRIVILEGES ON DB1_NHANSU.* TO 'app_user'@'localhost';
GRANT ALL PRIVILEGES ON DB2_LUONG.* TO 'app_user'@'localhost';

-- Apply changes
FLUSH PRIVILEGES;
```

#### B. Tạo 2 Database

```sql
-- Database 1: Nhân sự
CREATE DATABASE DB1_NHANSU CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Database 2: Lương
CREATE DATABASE DB2_LUONG CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

#### C. Import SQL Scripts

```bash
# Nếu dùng command line MySQL
mysql -u app_user -p DB1_NHANSU < sql/DB1_NhanSu.sql
mysql -u app_user -p DB2_LUONG < sql/DB2_Luong.sql

# Nhập password: app_secure_password_123
```

**Hoặc dùng MySQL Workbench:**
1. Open MySQL Workbench
2. Chọn Database → Query File
3. Load `sql/DB1_NhanSu.sql` → Execute
4. Load `sql/DB2_Luong.sql` → Execute

---

### 5️⃣ **Configure Environment Variables**

#### A. Tạo `.env` file

Copy từ `.env.example`:

```bash
cd backend
cp .env.example .env

# Hoặc trên Windows:
copy .env.example .env
```

#### B. Edit `.env` file

Mở `backend/.env` và kiểm tra:

```env
FLASK_ENV=development
FLASK_APP=wsgi.py

# Secret keys (giữ nguyên hoặc generate mới)
SECRET_KEY=9bJ7kL2mN5pQ8xW3yZ1aB4cD6eF9gH2jK5mN8pQ1rS4tU7vW0xY3zC6dE9fG2h
JWT_SECRET_KEY=3kL7mN1pQ5xW9yZ2aB6cD4eF8gH3jK7mN2pQ9rS3tU6vW1xY4zC7dE2fG5h

# Database URLs (nếu MySQL server chạy ở localhost, giữ nguyên)
DATABASE_URL_DB1=mysql+pymysql://app_user:app_secure_password_123@localhost/DB1_NHANSU
DATABASE_URL_DB2=mysql+pymysql://app_user:app_secure_password_123@localhost/DB2_LUONG

# MySQL Connection Info
MYSQL_HOST=localhost
MYSQL_USER=app_user
MYSQL_PASSWORD=app_secure_password_123
MYSQL_DB1=DB1_NHANSU
MYSQL_DB2=DB2_LUONG
```

**⚠️ Nếu MySQL server chạy ở máy khác:**
- Thay `localhost` → IP hoặc hostname của MySQL server
- Ví dụ: `192.168.1.100` hoặc `mysql.company.local`

---

### 6️⃣ **Chạy Flask Server**

```bash
# Đảm bảo đang trong backend folder
cd backend

# Activate virtual environment (nếu chưa)
# Windows: myENV\Scripts\activate
# Linux/macOS: source myENV/bin/activate

# Chạy server
python wsgi.py
```

**Kết quả mong đợi:**
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.1.x:5000
```

---

### 7️⃣ **Test API**

#### Dùng REST Client (VS Code Extension)

1. Install extension: **REST Client** (by Huachao Mao)
2. Mở file `backend/test.http`
3. Click "Send Request" ở request #1 (LOGIN - ADMIN)
4. Copy token từ response
5. Paste vào line 5: `@token = [TOKEN_MỚI]`
6. Test request #4 (GET DANH SÁCH NHÂN VIÊN)

#### Hoặc dùng Postman

1. Import file: `CSDLPT_API.postman_collection.json`
2. Click Login → Server sẽ tự-save token
3. Test các endpoint khác

---

## 🔧 Troubleshooting

### ❌ Lỗi: "Connection refused" (MySQL)

**Nguyên nhân:** MySQL server không chạy

**Fix:**
```bash
# Windows - Start MySQL Service
net start MySQL80

# macOS
brew services start mysql

# Linux
sudo systemctl start mysql
```

### ❌ Lỗi: "Subject must be a string"

**Nguyên nhân:** Token cũ/hết hạn

**Fix:** Login lại để lấy token mới → Copy vào test.http → Test lại

### ❌ Lỗi: "UnboundExecutionError: SQLALCHEMY_DATABASE_URI not set"

**Nguyên nhân:** .env file không được load

**Fix:**
1. Kiểm tra `.env` file có trong `backend/` folder không
2. Kiểm tra FLASK_ENV=development
3. Restart Flask server

### ❌ Lỗi: "Access denied for user 'app_user'"

**Nguyên nhân:** MySQL user/password sai

**Fix:**
1. Kiểm tra .env: MYSQL_USER, MYSQL_PASSWORD
2. Test kết nối:
```bash
mysql -u app_user -p -h localhost
# Nhập password: app_secure_password_123
```

---

## 📋 Test Accounts

Sau khi setup thành công, có 3 test users:

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Admin |
| ketoan | ketoan123 | Kế toán (Accountant) |
| nhanvien | nhanvien123 | Nhân viên (Employee) |

---

## 🔐 Security Notes

**Cho Development:**
- Secret keys có thể giữ nguyên
- Hardcoded users OK cho testing

**Cho Production:**
1. Đổi SECRET_KEY và JWT_SECRET_KEY (generate random)
2. Tạo MySQL user riêng với quyền hạn chế
3. Dùng environment variables hoặc Secret Manager
4. Enable HTTPS
5. Disable Debug mode

---

## 📞 Liên hệ Support

Nếu gặp vấn đề:
1. Kiểm tra troubleshooting section trên
2. Kiểm tra Flask server logs
3. Verify MySQL connection
4. Contact: [Team Lead Email]

---

## ✅ Checklist

- [ ] Clone repository
- [ ] Tạo virtual environment
- [ ] Install dependencies
- [ ] Tạo 2 MySQL databases
- [ ] Tạo app_user MySQL account
- [ ] Import SQL scripts
- [ ] Tạo .env file từ .env.example
- [ ] Chạy Flask server
- [ ] Test login endpoint
- [ ] Test GET /api/nhanvien endpoint
- [ ] Có được data từ database ✅

**Nếu all checkboxes ✅ → Setup thành công!**
