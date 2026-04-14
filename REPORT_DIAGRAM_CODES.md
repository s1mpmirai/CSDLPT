# Mã Sơ Đồ Báo Cáo (Mermaid)

Các sơ đồ dưới đây đã được căn theo mô tả bảng trong tài liệu TRƯỜNG ĐẠI HỌC.docx (bản trích xuất `TRUONG_DAI_HOC_extracted.txt`), đặc biệt ở các mục 3.2, 3.3, 3.4, 4.1, 4.2, 4.3, 4.4 và 4.8.

## Giải Thích Chi Tiết Mục 2.4 (Phân Tán CSDL)

### 1) Phân mảnh dữ liệu (Fragmentation)
- Hệ thống phân mảnh theo chiều dọc theo domain nghiệp vụ, không phải chia ngang theo bản ghi.
- DB1_NHANSU chỉ lưu dữ liệu nhân sự và tổ chức: NhanVien, PhongBan, ChucVu.
- DB2_LUONG chỉ lưu dữ liệu tiền lương: BangLuong, ChiTietLuongThang, BaoHiemConfig, LichSuThayDoiLuong, HopDongLuong.
- Liên kết logic giữa hai DB đi qua khóa NhanVienID (không dùng foreign key vật lý liên database trong MySQL).

### 2) Tính trong suốt dữ liệu (Transparency)
- Người dùng và frontend không truy vấn trực tiếp từng DB; chỉ gọi API.
- Backend thực hiện "hợp nhất dữ liệu" theo 2 cách:
  - Cách 1: View cross-DB (ví dụ vw_AdminNhanVienDayDu) để đọc dữ liệu tổng hợp một lần.
  - Cách 2: API merge (đọc DB1 và DB2 riêng, ghép theo NhanVienID rồi trả về một JSON duy nhất).
- Vì vậy, UI chỉ thấy một mô hình dữ liệu thống nhất, không cần biết bản ghi đến từ DB1 hay DB2.

### 3) Đồng bộ thao tác (Consistency/Sync)
- Với các nghiệp vụ chạm cả 2 DB (thêm nhân viên, xóa mềm nhân viên), backend coi đây là một đơn vị công việc logic.
- Luồng thêm nhân viên:
  - B1: Insert NhanVien vào DB1_NHANSU.
  - B2: Insert BangLuong mặc định vào DB2_LUONG.
  - B3: Nếu cả hai thành công thì commit; nếu một bước lỗi thì rollback để tránh lệch dữ liệu.
- Luồng xóa mềm:
  - B1: Update NhanVien.TrangThai = 0 ở DB1.
  - B2: Update BangLuong.TrangThai = 0 ở DB2.
  - B3: Ghi nhận lịch sử thay đổi lương và hoàn tất giao dịch.
- Mục tiêu là đảm bảo: không có trường hợp nhân viên tồn tại ở DB1 nhưng thiếu hồ sơ lương ở DB2 (hoặc ngược lại ở trạng thái hoạt động).

### 4) Phân quyền (Authorization)
- Bảo mật theo 2 lớp:
  - Lớp API: JWT + kiểm tra role trước khi xử lý nghiệp vụ.
  - Lớp dữ liệu: quyền truy cập bảng/DB theo vai trò nghiệp vụ.
- Admin chủ yếu quản trị dữ liệu nhân sự và xem báo cáo tổng hợp.
- Kế toán tập trung thao tác dữ liệu lương.
- Nhân viên chỉ được xem dữ liệu của chính mình (lọc theo user_id trong token).

### 5) Hai DB "giao tiếp" với nhau như thế nào trong thực tế?
- Hai DB không gọi trực tiếp nhau như service-to-service; chúng được điều phối bởi backend Flask.
- Backend đóng vai trò "orchestrator":
  - Điều phối ghi nhiều bước giữa DB1 và DB2.
  - Gom dữ liệu từ nhiều nguồn thành một response thống nhất.
  - Áp dụng rule nghiệp vụ và rule phân quyền trước khi trả dữ liệu.
- Ngoài backend, một số truy vấn đọc có thể dùng view cross-DB để tăng tính trong suốt khi báo cáo.

### 6) Luồng tương tác chuẩn giữa 2 DB
- Luồng ghi (write path): Frontend -> API -> DB1 + DB2 -> commit/rollback -> API response.
- Luồng đọc (read path): Frontend -> API -> (DB1, DB2 hoặc view cross-DB) -> merge -> JSON trả về UI.

## 1) Kiến Trúc Tổng Thể Hệ Thống (3 Lớp)
```mermaid
flowchart LR
  subgraph P[Presentation Layer]
    FE[Web Frontend\nHTML CSS JS]
  end

  subgraph B[Business Logic Layer]
    API[Flask Backend\nRoutes + Services]
    AUTH[JWT Auth + Role Check]
    MERGE[API Merge DB1 + DB2]
  end

  subgraph D[Data Layer]
    DB1[(DB1_NHANSU)]
    DB2[(DB2_LUONG)]
  end

  FE --> API
  API --> AUTH
  API --> MERGE
  API --> DB1
  API --> DB2
```

## 2) Phân Mảnh Dọc Dữ Liệu (Vertical Fragmentation)
```mermaid
flowchart TB
  A[HR Payroll Domain] --> B[DB1_NHANSU\nMiền Nhân sự]
  A --> C[DB2_LUONG\nMiền Tiền lương]

  B --> B1[NhanVien\nNhanVienID HoTen NgaySinh GioiTinh\nPhongBanID ChucVuID TrangThai]
  B --> B2[PhongBan\nPhongBanID TenPhongBan MoTa]
  B --> B3[ChucVu\nChucVuID TenChucVu MoTa]

  C --> C1[BangLuong\nBangLuongID NhanVienID LuongCoBan\nPhuCap TrangThai]
  C --> C2[ChiTietLuongThang\nChiTietID NhanVienID Thang Nam\nLuongThucLinh]
  C --> C3[BaoHiemConfig\nConfigID TyLeBHXH TyLeBHYT\nTyLeBHTN HieuLuc]
  C --> C4[LichSuThayDoiLuong\nLichSuID NhanVienID LuongCu LuongMoi\nNgayThayDoi]
  C --> C5[HopDongLuong\nHopDongID NhanVienID NgayBatDau\nNgayKetThuc LuongHopDong]

  B -. View cross DB .-> C
```

## 3) Use Case Tổng Hợp Theo Vai Trò
```mermaid
flowchart LR
  A[Admin]
  K[Kế toán]
  N[Nhân viên]

  subgraph SYS[HỆ THỐNG HR PAYROLL PHÂN TÁN]
    direction TB
    UC01([UC01 Đăng nhập])
    UC02([UC02 Xem Dashboard])
    UC03([UC03 Quản lý Nhân viên])
    UC04([UC04 Quản lý Phòng ban])
    UC05([UC05 Quản lý Chức vụ])
    UC06([UC06 Xem thông tin đầy đủ NV - vw_AdminNhanVienDayDu])
    UC07([UC07 Xem danh sách nhân viên])
    UC08([UC08 Quản lý Bảng lương])
    UC09([UC09 Tính lương tháng])
    UC10([UC10 Xem lịch sử lương])
    UC11([UC11 Quản lý Bảo hiểm])
    UC12([UC12 Xem báo cáo lương])
    UC13([UC13 Đăng nhập])
    UC14([UC14 Xem thông tin cá nhân])
    UC15([UC15 Xem phiếu lương])
    UC16([UC16 Xem lịch sử lương bản thân])
  end

  A --> UC01
  A --> UC02
  A --> UC03
  A --> UC04
  A --> UC05
  A --> UC06

  K --> UC07
  K --> UC08
  K --> UC09
  K --> UC10
  K --> UC11
  K --> UC12

  N --> UC13
  N --> UC14
  N --> UC15
  N --> UC16
```

## 4) Sequence - Đăng Nhập + JWT (3.4.1)
```mermaid
sequenceDiagram
  actor User
  participant FE as Frontend
  participant API as Flask API

  User->>FE: Nhập username/password
  FE->>API: POST /api/auth/login {username, password}
  API->>API: Kiểm tra tài khoản trong auth.py
  API->>API: Tạo JWT payload {user_id, role, exp}
  API-->>FE: {access_token, role, user_info}
  FE->>FE: Lưu token localStorage
  FE->>API: Các request sau kèm Authorization Bearer token
```

## 5) Sequence - Thêm Nhân Viên + Tạo Bảng Lương (3.4.2)
```mermaid
sequenceDiagram
  actor Admin
  participant FE as Frontend
  participant API as Flask API
  participant DB1 as DB1_NHANSU
  participant DB2 as DB2_LUONG

  Admin->>FE: Gửi form thêm nhân viên
  FE->>API: POST /api/nhanvien + JWT
  API->>API: Validate dữ liệu đầu vào
  API->>API: BEGIN TRANSACTION
  API->>DB1: INSERT NhanVien
  DB1-->>API: Trả NhanVienID mới
  API->>DB2: INSERT BangLuong\n(LuongCoBan=0, TrangThai=1)
  alt Thành công cả 2 DB
    API->>API: COMMIT
    API-->>FE: {success:true, nhanvien_id, bangluong_id}
  else Lỗi bất kỳ bước nào
    API->>API: ROLLBACK toàn bộ
    API-->>FE: 500 error
  end
```

## 6) Sequence - Tính Lương Tháng + Dashboard (3.4.3)
```mermaid
sequenceDiagram
  actor Ketoan as Kế toán
  participant FE as Frontend
  participant API as Flask API
  participant DB1 as DB1_NHANSU
  participant DB2 as DB2_LUONG

  Ketoan->>FE: Chọn tháng/năm cần tính lương
  FE->>API: POST /api/luong/chi-tiet {thang, nam}
  API->>DB1: Lấy NhanVien đang hoạt động (TrangThai=1)
  loop Mỗi nhân viên
    API->>DB2: Lấy BangLuong theo NhanVienID
    API->>DB2: Lấy BaoHiemConfig hiệu lực
    API->>API: Tính luong_thuc_lanh = luong_co_ban + phu_cap - bao_hiem - thue
    API->>DB2: INSERT ChiTietLuongThang
    API->>DB2: Cập nhật LichSuThayDoiLuong
  end
  FE->>API: GET /api/statistics
  API->>DB1: Đếm tổng nhân viên
  API->>DB2: Tính tổng quỹ lương
  API-->>FE: JSON thống kê dashboard
```

## 7) Activity - UC03 Thêm Nhân Viên Mới
```mermaid
flowchart TD
  S([Bắt đầu]) --> A[Admin nhập thông tin nhân viên]
  A --> B[Hệ thống validate dữ liệu]
  B --> C{Dữ liệu hợp lệ?}
  C -- Không --> X[Trả lỗi validate]
  X --> E([Kết thúc])
  C -- Có --> D[Insert NhanVien vào DB1_NHANSU]
  D --> F[Tạo BangLuong mặc định ở DB2_LUONG]
  F --> G{Bước tạo BangLuong thành công?}
  G -- Không --> H[Rollback bước insert DB1 và báo lỗi]
  H --> E
  G -- Có --> I[Trả kết quả thành công]
  I --> E
```

## 8) Activity - UC09 Tính Lương Tháng
```mermaid
flowchart TD
  S([Bắt đầu]) --> A[Kế toán chọn tháng/năm]
  A --> B[Lấy danh sách NV hoạt động từ DB1]
  B --> C{Còn nhân viên cần tính?}
  C -- Không --> H[Trả tổng kết thành công]
  H --> E([Kết thúc])
  C -- Có --> D[Lấy BangLuong và BaoHiemConfig từ DB2]
  D --> F[Tính lương thực lĩnh]
  F --> G[Insert ChiTietLuongThang + cập nhật LichSuThayDoiLuong]
  G --> C
```

## 9) ER Diagram Theo Bảng Mô Tả (4.2)
```mermaid
erDiagram
  PHONGBAN ||--o{ NHANVIEN : "contains"
  CHUCVU ||--o{ NHANVIEN : "assigns"
  NHANVIEN ||--o| BANGLUONG : "has"
  NHANVIEN ||--o{ CHITIETLUONGTHANG : "receives"
  NHANVIEN ||--o{ LICHSUTHAYDOILUONG : "changes"
  NHANVIEN ||--o{ HOPDONGLUONG : "contracts"

  NHANVIEN {
    int NhanVienID PK
    string HoTen
    date NgaySinh
    string GioiTinh
    string Email
    int PhongBanID FK
    int ChucVuID FK
    int TrangThai
  }
  PHONGBAN {
    int PhongBanID PK
    string TenPhongBan
    string MoTa
  }
  CHUCVU {
    int ChucVuID PK
    string TenChucVu
    string MoTa
  }
  BANGLUONG {
    int BangLuongID PK
    int NhanVienID FK
    decimal LuongCoBan
    decimal PhuCap
    int TrangThai
  }
  CHITIETLUONGTHANG {
    int ChiTietID PK
    int NhanVienID FK
    int Thang
    int Nam
    decimal LuongThucLinh
  }
  BAOHIEMCONFIG {
    int ConfigID PK
    float TyLeBHXH
    float TyLeBHYT
    float TyLeBHTN
    int HieuLuc
  }
  LICHSUTHAYDOILUONG {
    int LichSuID PK
    int NhanVienID FK
    decimal LuongCu
    decimal LuongMoi
    date NgayThayDoi
  }
  HOPDONGLUONG {
    int HopDongID PK
    int NhanVienID FK
    date NgayBatDau
    date NgayKetThuc
    decimal LuongHopDong
  }
```

## 10) Tính Trong Suốt Dữ Liệu (View + API Merge) (4.3)
```mermaid
flowchart LR
  FE[Frontend]
  API[Flask API]
  V[vw_AdminNhanVienDayDu]
  DB1[(DB1_NHANSU)]
  DB2[(DB2_LUONG)]
  M[API merge layer]

  FE --> API
  API --> V
  V --> DB1
  V --> DB2

  API --> M
  M --> DB1
  M --> DB2

  API --> R1[GET /api/statistics]
  API --> R2[GET /api/luong/danh-sach]
```

## 11) Use Case Chi Tiết - Admin (3.2.1)
```mermaid
flowchart LR
  A((Admin))

  UC01[UC01 Đăng nhập]
  UC02[UC02 Xem Dashboard]
  UC03[UC03 Quản lý Nhân viên]
  UC04[UC04 Quản lý Phòng ban]
  UC05[UC05 Quản lý Chức vụ]
  UC06["UC06 Xem thông tin đầy đủ NV<br/>vw_AdminNhanVienDayDu"]

  A --> UC01
  A --> UC02
  A --> UC03
  A --> UC04
  A --> UC05
  A --> UC06
```

## 12) Use Case Chi Tiết - Kế Toán (3.2.2)
```mermaid
flowchart LR
  K((Kế toán))

  UC07[UC07 Xem danh sách nhân viên]
  UC08[UC08 Quản lý Bảng lương]
  UC09[UC09 Tính lương tháng]
  UC10[UC10 Xem lịch sử lương]
  UC11[UC11 Quản lý Bảo hiểm]
  UC12[UC12 Xem báo cáo lương]

  K --> UC07
  K --> UC08
  K --> UC09
  K --> UC10
  K --> UC11
  K --> UC12
```

## 13) Use Case Chi Tiết - Nhân Viên (3.2.3)
```mermaid
flowchart LR
  N((Nhân viên))

  UC13[UC13 Đăng nhập]
  UC14[UC14 Xem thông tin cá nhân]
  UC15[UC15 Xem phiếu lương]
  UC16[UC16 Xem lịch sử lương bản thân]

  N --> UC13
  N --> UC14
  N --> UC15
  N --> UC16
```

## 14) Sequence - Xem Chi Tiết Lương + Role Guard
```mermaid
sequenceDiagram
  actor NV as Nhân viên
  participant FE as Frontend
  participant API as Flask API
  participant DB2 as DB2_LUONG
  participant DB1 as DB1_NHANSU

  NV->>FE: Mở phiếu lương theo id
  FE->>API: GET /api/luong/chi-tiet/{id} + JWT
  API->>API: Decode token, đọc role và user_id
  API->>DB2: Lấy ChiTietLuongThang theo id
  alt role = nhanvien và NhanVienID không khớp user_id
    API-->>FE: 403 Forbidden
  else Được phép truy cập
    API->>DB1: Lấy thông tin NV từ DB1
    API-->>FE: 200 payroll detail JSON
  end
```

## 15) Activity - Xóa Mềm Nhân Viên Đồng Bộ (4.4.2)
```mermaid
flowchart TD
  S([Bắt đầu]) --> A[Admin gửi yêu cầu xóa NV]
  A --> B[Update DB1_NHANSU.NhanVien TrangThai=0]
  B --> C[Update DB2_LUONG.BangLuong TrangThai=0]
  C --> D[Ghi LichSuThayDoiLuong\nGhi chú: Nhân viên nghỉ việc]
  D --> E{Có lỗi trong quá trình cập nhật?}
  E -- Có --> F[Rollback, giữ nguyên trạng thái cũ]
  F --> H([Kết thúc])
  E -- Không --> G[Commit và trả về thành công]
  G --> H
```

## 16) Luồng Điều Hướng Frontend -> Backend (4.8)
```mermaid
flowchart TD
  L[Trang đăng nhập] -->|POST /api/auth/login| D[Dashboard]

  D --> M1[Danh sách nhân viên]
  D --> M2[Chi tiết nhân viên]
  D --> M3[Bảng lương]
  D --> M4[Phiếu lương]
  D --> M5[Thống kê]

  M1 -->|API| A1[/api/nhanvien]
  M2 -->|API| A2[/api/nhanvien/{id}]
  M3 -->|API| A3[/api/luong/danh-sach]
  M4 -->|API| A4[/api/luong/chi-tiet]
  M5 -->|API| A5[/api/statistics]

  D -->|Đăng xuất| L
```

## Gợi Ý Vị Trí Đặt Trong Báo Cáo
1. Hình 1 (Kiến trúc tổng thể 3 lớp) -> Chương 4.1
2. Hình 2 (Phân mảnh dọc dữ liệu) -> Chương 4.2
3. Hình 3 (Use Case tổng hợp theo vai trò) -> Chương 3.2
4. Hình 4 (Sequence Đăng nhập + JWT) -> Chương 3.4.1
5. Hình 5 (Sequence Thêm nhân viên + Tạo bảng lương) -> Chương 3.4.2
6. Hình 6 (Sequence Tính lương tháng + Dashboard) -> Chương 3.4.3
7. Hình 7 (Activity UC03 Thêm nhân viên) -> Chương 3.3
8. Hình 8 (Activity UC09 Tính lương tháng) -> Chương 3.3
9. Hình 9 (ER Diagram theo bảng mô tả) -> Chương 4.2
10. Hình 10 (Tính trong suốt dữ liệu) -> Chương 4.3
11. Hình 11 (Use Case chi tiết Admin) -> Chương 3.2.1
12. Hình 12 (Use Case chi tiết Kế toán) -> Chương 3.2.2
13. Hình 13 (Use Case chi tiết Nhân viên) -> Chương 3.2.3
14. Hình 14 (Sequence Xem chi tiết lương + Role Guard) -> Chương 3.4.4 (bổ sung)
15. Hình 15 (Activity Xóa mềm đồng bộ) -> Chương 4.4.2
16. Hình 16 (Luồng Frontend -> Backend) -> Chương 4.8
