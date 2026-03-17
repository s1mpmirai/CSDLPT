# HR PAYROLL - Hệ thống Quản lý Nhân sự & Tiền lương

Hệ thống được thiết kế theo mô hình **Cơ sở dữ liệu phân tán (Phân mảnh dọc)** nhằm tách biệt dữ liệu hành chính và dữ liệu tài chính nhạy cảm, đảm bảo tính bảo mật và toàn vẹn dữ liệu.

## 🚀 Tài khoản thử nghiệm (Test Accounts)

Dưới đây là các tài khoản mặc định để kiểm tra các chức năng phân quyền:

| Tài khoản | Mật khẩu | Vai trò | Chức năng chính |
| :--- | :--- | :--- | :--- |
| `admin` | `admin123` | **Admin** | Quản lý nhân viên (CRUD), xem thống kê tổng hợp (View), quản lý hệ thống. |
| `ketoan` | `ketoan123` | **Kế toán** | Quản lý bảng lương, tính lương tháng, xem chi tiết lương toàn công ty. |
| `nhanvien` | `nhanvien123` | **Nhân viên** | Xem thông tin cá nhân và tra cứu lịch sử lương của chính mình. |

## 🛠️ Mô hình chức năng theo Vai trò

### 1. Vai trò Quản trị viên (Admin)
- **Quản lý Nhân viên**: Thêm mới, sửa thông tin và xóa (nghỉ việc) nhân viên.
- **Tính trong suốt**: Nhờ View liên database, Admin có thể xem danh sách nhân sự kèm theo mức lương cơ bản dù dữ liệu nằm ở 2 DB khác nhau.
- **Đồng bộ hóa**: Khi thêm nhân viên ở giao diện Admin, hệ thống tự động khởi tạo bản ghi lương bên DB2.

### 2. Vai trò Kế toán (Accountant)
- **Quản lý Bảng lương**: Xem danh sách lương của toàn bộ nhân viên trong công ty.
- **Tính lương tháng**: Thực hiện tính toán lương thực lĩnh (bao gồm phụ cấp, tăng ca, bảo hiểm và phạt) cho một hoặc tất cả nhân viên.
- **Tìm kiếm**: Tra cứu nhanh thông tin lương theo tên nhân viên hoặc email.

### 3. Vai trò Nhân viên (Employee)
- **Lương của tôi**: Giao diện được tối ưu hóa chỉ hiển thị dữ liệu cá nhân.
- **Bảo mật**: Nhân viên không thể xem thông tin của người khác và không thấy các thẻ thông số tài chính của toàn công ty trên trang chủ.
- **Chi tiết lương**: Xem bảng kê chi tiết các khoản thu nhập và khấu trừ hàng tháng.

## ⚙️ Hướng dẫn cài đặt và khởi chạy

### 1. Chuẩn bị Cơ sở dữ liệu
Hệ thống sử dụng **MySQL**. Bạn cần chạy 2 file script SQL trong thư mục `backend/sql` theo thứ tự:
1. Chạy `DB1_NhanSu.sql` để tạo CSDL nhân sự.
2. Chạy `DB2_Luong.sql` để tạo CSDL lương và thiết lập phân quyền user.

### 2. Cấu hình và Chạy Backend (API)
1. Di chuyển vào thư mục backend:
   ```bash
   cd backend
   ```
2. Cài đặt các thư viện cần thiết:
   ```bash
   pip install -r requirements.txt
   ```
3. Tạo file `.env` từ file mẫu `.env.example` và cấu hình thông tin kết nối MySQL (DB_USER, DB_PASSWORD).
4. Khởi chạy server:
   ```bash
   python wsgi.py
   ```
   *Mặc định API sẽ chạy tại: `http://localhost:5000`*

### 3. Chạy Frontend (Giao diện)
1. Di chuyển vào thư mục frontend:
   ```bash
   cd web-frontend
   ```
2. Khởi chạy server web đơn giản bằng Python:
   ```bash
   python -m http.server 8000
   ```
3. Truy cập vào trình duyệt: `http://localhost:8000`

### 4. Khởi chạy bằng Docker (Ưu tiên)
Nếu bạn đã cài đặt **Docker** và **Docker Compose**, bạn có thể chạy toàn bộ hệ thống (bao gồm 2 CSDL, Backend và Frontend) chỉ với một câu lệnh:
1. Đảm bảo bạn đang ở thư mục gốc của dự án.
2. Chạy câu lệnh:
   ```bash
   docker-compose up --build
   ```
3. Truy cập:
   - Frontend: `http://localhost:8000`
   - Backend API: `http://localhost:5000`
   - MySQL: `localhost:3306` (user: `root`, pass: `root_password`)

* Docker sẽ tự động thiết lập 2 CSDL riêng biệt và khởi tạo các bảng, view, và dữ liệu mẫu cần thiết.*

## 🏗️ Kiến trúc kỹ thuật
- **Frontend**: HTML5, CSS3 (Glassmorphism), Vanilla JavaScript.
- **Backend**: Python Flask RESTful API, JWT Authentication.
- **Database**: MySQL (Phân mảnh dọc thành 2 DB vật lý: `DB1_NHANSU` và `DB2_LUONG`).
