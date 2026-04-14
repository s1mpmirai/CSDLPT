# Huong dan chuyen bao cao mau sang CSDLPT hien tai

## Muc tieu
Tai lieu nay chi ra ro:
- Phan nao can bo trong mau bao cao cu (de tai banh ngot + SQLite)
- Phan nao can them vao de dung voi project HR Payroll phan tan (DB1_NHANSU + DB2_LUONG)

## 1) Bo hoan toan khoi bao cao mau
- Toan bo noi dung lien quan den cua hang banh ngot, san pham banh, gio hang, thanh toan ban le.
- Toan bo use case va sequence cho cac module: San pham, Khach hang, Ban hang, Hoa don ban le, Phieu nhap/huy kho banh.
- Toan bo mo ta CSDL SQLite va cac bang phuc vu domain banh ngot (products, invoice, import_invoice, type_product, ...).
- Toan bo hinh UI cua domain banh ngot.
- Toan bo bang bieu ten cu thuoc domain banh ngot.

## 2) Giu cau truc chuong, thay noi dung
- Chuong 1 (Tong quan): doi ten de tai thanh he thong quan ly nhan su - tien luong phan tan.
- Chuong 2 (Thu thap yeu cau): doi nghiep vu ve HR va Payroll.
- Chuong 3 (Phan tich): doi actor, use case, dac ta va sequence theo 3 vai tro admin/ketoan/nhanvien.
- Chuong 4 (Thiet ke): doi class model, CSDL quan he, va giao dien theo web frontend hien tai.
- Chuong 5 (Cai dat): doi stack ky thuat theo Flask + MySQL + web frontend.
- Chuong 6 (Phan cong): giu nguyen form, cap nhat task theo cong viec thuc te trong repo.
- Chuong 7 (Ket luan): viet lai theo ket qua dat duoc cua he thong phan tan.

## 3) Them moi bat buoc (quan trong nhat)

### 3.1 Kien truc phan tan CSDL
- Mo ta phan manh doc:
  - DB1_NHANSU: NhanVien, PhongBan, ChucVu
  - DB2_LUONG: BangLuong, ChiTietLuongThang, BaoHiemConfig, LichSuThayDoiLuong, HopDongLuong
- Trinh bay SQLAlchemy binds trong backend config.
- Trinh bay ly do tach domain du lieu nhan su va du lieu luong.

### 3.2 Tinh trong suot du lieu (transparency)
- Them phan mo ta view cross-db:
  - vw_AdminNhanVienDayDu (DB1 join DB2_LUONG.BangLuong)
- Them phan mo ta transparency o tang API (backend merge du lieu DB1 + DB2 khi tra ve frontend).

### 3.3 Dong bo thao tac (consistency/sync)
- Them phan mo ta luong them nhan vien:
  - Insert DB1 NhanVien
  - Tao BangLuong mac dinh o DB2
- Them phan mo ta luong xoa mem nhan vien:
  - TrangThai=0 o DB1
  - TrangThai=0 o DB2 BangLuong
- Neu co, mo ta rollback neu loi transaction.

### 3.4 Bao mat va phan quyen
- Vai tro: admin, ketoan, nhanvien.
- JWT auth + role-based access.
- Ranh gioi quyen xem/sua theo tung role.
- SQL grants (user_nhanvien, user_ketoan) trong script DB1.

### 3.5 API contract va frontend flow
- Dang nhap: /api/auth/login
- Dashboard thong ke: /api/statistics
- Nhan vien: /api/nhanvien
- Luong: /api/luong, /api/luong/danh-sach, /api/luong/chi-tiet
- Phong ban/chuc vu: /api/phongban, /api/chucvu
- Mo ta ro map frontend -> api-client -> backend route -> model -> table.

### 3.6 Trien khai va van hanh
- Local run backend + frontend.
- Docker compose run all services.
- Thu tu init SQL (DB2 truoc DB1) khi can tao cross-db dependencies.

## 4) Danh sach hinh/bang nen co trong bao cao moi
- So do kien truc tong the (Web frontend, Flask API, DB1, DB2).
- So do phan manh du lieu (bang nao thuoc DB nao).
- So do luong nghiep vu theo role (admin/ketoan/nhanvien).
- Sequence cho 3 luong trong tam:
  - Login + JWT
  - Them nhan vien + tao bang luong
  - Tinh luong thang + hien thi dashboard
- Bang mapping API endpoint -> role -> bang du lieu tac dong.
- Bang test case cho 4 yeu cau: phan manh, trong suot, dong bo, phan quyen.

## 5) Mapping nhanh keyword de thay trong Word
- Tim va xoa/cap nhat cac tu khoa cu:
  - "banh ngot", "san pham", "khach hang", "hoa don", "phieu nhap", "SQLite"
- Thay bang keyword moi:
  - "nhan vien", "phong ban", "chuc vu", "bang luong", "chi tiet luong", "DB1_NHANSU", "DB2_LUONG", "Flask", "MySQL", "JWT"

## 6) Nguon doi chieu trong repo hien tai
- Tong quan va setup: README.md
- Bao cao phan manh: BAOCAO_PHANMANH.md
- Kien truc backend: backend/app/__init__.py, backend/config.py
- Model DB1: backend/app/models/nhanvien.py
- Model DB2: backend/app/models/luong.py
- Route API: backend/app/routes/*.py
- SQL DB1: backend/sql/DB1_NhanSu.sql
- SQL DB2: backend/sql/DB2_Luong.sql
- Frontend flow: web-frontend/js/api-client.js, web-frontend/js/dashboard.js

## 7) De cuong chuong muc de xai ngay
- Chuong 1: Gioi thieu de tai HR Payroll phan tan
- Chuong 2: Khao sat va yeu cau he thong
- Chuong 3: Phan tich use case theo role
- Chuong 4: Thiet ke kien truc + CSDL phan tan + API + UI
- Chuong 5: Cai dat va trien khai
- Chuong 6: Kiem thu va danh gia theo 4 yeu cau de bai
- Chuong 7: Ket luan, uu diem, han che, huong phat trien
