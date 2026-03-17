-- =====================================================
-- DATABASE 1: DB1_NHANSU
-- Chứa thông tin Nhân viên, Phòng ban, Chức vụ
-- =====================================================

DROP DATABASE IF EXISTS DB1_NHANSU;
CREATE DATABASE DB1_NHANSU;
USE DB1_NHANSU;

-- =====================================================
-- 1. BẢNG PHÒNG BAN
-- =====================================================
CREATE TABLE PhongBan (
    MaPhong INT PRIMARY KEY AUTO_INCREMENT,
    TenPhong NVARCHAR(100) NOT NULL UNIQUE,
    TruongPhong NVARCHAR(100),
    CreateDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    UpdateDate DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- =====================================================
-- 2. BẢNG CHỨC VỤ
-- =====================================================
CREATE TABLE ChucVu (
    MaChucVu INT PRIMARY KEY AUTO_INCREMENT,
    TenChucVu NVARCHAR(100) NOT NULL UNIQUE,
    CreateDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    UpdateDate DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- =====================================================
-- 3. BẢNG NHÂN VIÊN
-- =====================================================
CREATE TABLE NhanVien (
    MaNV INT PRIMARY KEY AUTO_INCREMENT,
    TenNV NVARCHAR(100) NOT NULL,
    NgaySinh DATE NOT NULL,
    GioiTinh NVARCHAR(10) CHECK (GioiTinh IN (N'Nam', N'Nữ')),
    DiaChi NVARCHAR(255),
    SDT NVARCHAR(20),
    Email NVARCHAR(100) NOT NULL UNIQUE,
    MaPhong INT NOT NULL,
    MaChucVu INT NOT NULL,
    NgayVaoLam DATE NOT NULL,
    TrangThai INT DEFAULT 1 CHECK (TrangThai IN (0, 1)), -- 1: Đang làm, 0: Nghỉ việc
    CreateDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    UpdateDate DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (MaPhong) REFERENCES PhongBan(MaPhong) ON DELETE RESTRICT,
    FOREIGN KEY (MaChucVu) REFERENCES ChucVu(MaChucVu) ON DELETE RESTRICT,
    INDEX idx_Email (Email),
    INDEX idx_MaPhong (MaPhong),
    INDEX idx_MaChucVu (MaChucVu),
    INDEX idx_TrangThai (TrangThai)
);

-- =====================================================
-- SEED DATA CHO DB1
-- =====================================================

-- Thêm phòng ban
INSERT INTO PhongBan (TenPhong, TruongPhong) VALUES
(N'Kỹ Thuật', N'Nguyễn Văn A'),
(N'Kế Toán', N'Trần Thị B'),
(N'Nhân Sự', N'Lê Văn C'),
(N'Marketing', N'Phạm Thị D'),
(N'Bán Hàng', N'Hoàng Văn E');

-- Thêm chức vụ
INSERT INTO ChucVu (TenChucVu) VALUES
(N'Giám đốc'),
(N'Trưởng phòng'),
(N'Nhân viên'),
(N'Thực tập sinh');

-- Thêm nhân viên
INSERT INTO NhanVien (TenNV, NgaySinh, GioiTinh, DiaChi, SDT, Email, MaPhong, MaChucVu, NgayVaoLam, TrangThai) VALUES
(N'Nguyễn Văn A', '1990-05-15', N'Nam', N'123 Đường ABC, TP HCM', '0901234567', 'nguyenvana@company.com', 1, 2, '2020-01-15', 1),
(N'Trần Thị B', '1992-08-20', N'Nữ', N'456 Đường DEF, TP HCM', '0912345678', 'tranthib@company.com', 2, 2, '2020-03-20', 1),
(N'Lê Văn C', '1988-12-10', N'Nam', N'789 Đường GHI, TP HCM', '0923456789', 'levanc@company.com', 3, 2, '2019-06-10', 1),
(N'Phạm Thị D', '1995-03-25', N'Nữ', N'321 Đường JKL, TP HCM', '0934567890', 'phamthid@company.com', 4, 3, '2021-02-01', 1),
(N'Hoàng Văn E', '1993-07-30', N'Nam', N'654 Đường MNO, TP HCM', '0945678901', 'hoangvane@company.com', 5, 3, '2020-09-15', 1),
(N'Vũ Thị F', '1994-11-08', N'Nữ', N'987 Đường PQR, TP HCM', '0956789012', 'vuthif@company.com', 1, 3, '2021-04-10', 1),
(N'Đặng Văn G', '1996-02-14', N'Nam', N'246 Đường STU, TP HCM', '0967890123', 'dangvang@company.com', 2, 3, '2022-01-20', 1),
(N'Bùi Thị H', '1997-06-18', N'Nữ', N'135 Đường VWX, TP HCM', '0978901234', 'buithih@company.com', 3, 3, '2022-06-15', 1);

-- =====================================================
-- VIEWS CHO DB1
-- =====================================================

-- View: Thông tin nhân viên đầy đủ
CREATE VIEW vw_NhanVienDayDu AS
SELECT 
    nv.MaNV,
    nv.TenNV,
    nv.NgaySinh,
    nv.GioiTinh,
    nv.DiaChi,
    nv.SDT,
    nv.Email,
    pb.MaPhong,
    pb.TenPhong,
    cv.MaChucVu,
    cv.TenChucVu,
    nv.NgayVaoLam,
    nv.TrangThai,
    DATEDIFF(CURDATE(), nv.NgaySinh) / 365 AS Tuoi,
    nv.CreateDate,
    nv.UpdateDate
FROM NhanVien nv
INNER JOIN PhongBan pb ON nv.MaPhong = pb.MaPhong
INNER JOIN ChucVu cv ON nv.MaChucVu = cv.MaChucVu;

-- View: Báo cáo lương chi tiết (JOIN sang DB2)
-- Requirement 2: Tính trong suốt (Transparency) - Admin xem JOIN tự động
CREATE VIEW vw_AdminNhanVienDayDu AS
SELECT 
    nv.MaNV,
    nv.TenNV,
    pb.TenPhong,
    cv.TenChucVu,
    l.LuongCoBan,
    l.HeSoLuong,
    l.PhuCapChucVu,
    l.PhuCapPhongBan,
    (l.LuongCoBan * l.HeSoLuong + l.PhuCapChucVu + l.PhuCapPhongBan) AS TongThuNhap
FROM NhanVien nv
INNER JOIN PhongBan pb ON nv.MaPhong = pb.MaPhong
INNER JOIN ChucVu cv ON nv.MaChucVu = cv.MaChucVu
LEFT JOIN DB2_LUONG.BangLuong l ON nv.MaNV = l.MaNV;

-- View: Nhân viên theo phòng ban
CREATE VIEW vw_NhanVienTheoPhongBan AS
SELECT 
    pb.MaPhong,
    pb.TenPhong,
    pb.TruongPhong,
    COUNT(nv.MaNV) AS SoNhanVien,
    SUM(CASE WHEN nv.TrangThai = 1 THEN 1 ELSE 0 END) AS SoNhanVienDangLam
FROM PhongBan pb
LEFT JOIN NhanVien nv ON pb.MaPhong = nv.MaPhong
GROUP BY pb.MaPhong, pb.TenPhong, pb.TruongPhong;

-- =====================================================
-- STORED PROCEDURES CHO DB1
-- =====================================================

-- Procedure: Thêm nhân viên mới vào DB1 (sẽ được gọi từ Backend)
DELIMITER $$
CREATE PROCEDURE sp_ThemNhanVien(
    IN p_TenNV NVARCHAR(100),
    IN p_NgaySinh DATE,
    IN p_GioiTinh NVARCHAR(10),
    IN p_DiaChi NVARCHAR(255),
    IN p_SDT NVARCHAR(20),
    IN p_Email NVARCHAR(100),
    IN p_MaPhong INT,
    IN p_MaChucVu INT,
    IN p_NgayVaoLam DATE,
    OUT p_MaNV INT,
    OUT p_Message NVARCHAR(255)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        SET p_Message = N'Lỗi: Email đã tồn tại hoặc dữ liệu không hợp lệ';
        SET p_MaNV = 0;
    END;
    
    -- Kiểm tra email đã tồn tại
    IF EXISTS (SELECT 1 FROM NhanVien WHERE Email = p_Email) THEN
        SET p_Message = N'Email đã tồn tại';
        SET p_MaNV = 0;
    ELSE
        INSERT INTO NhanVien (TenNV, NgaySinh, GioiTinh, DiaChi, SDT, Email, MaPhong, MaChucVu, NgayVaoLam, TrangThai)
        VALUES (p_TenNV, p_NgaySinh, p_GioiTinh, p_DiaChi, p_SDT, p_Email, p_MaPhong, p_MaChucVu, p_NgayVaoLam, 1);
        
        SET p_MaNV = LAST_INSERT_ID();
        SET p_Message = N'Thêm nhân viên thành công';
    END IF;
END$$
DELIMITER ;

-- Procedure: Cập nhật thông tin nhân viên
DELIMITER $$
CREATE PROCEDURE sp_CapNhatNhanVien(
    IN p_MaNV INT,
    IN p_TenNV NVARCHAR(100),
    IN p_DiaChi NVARCHAR(255),
    IN p_SDT NVARCHAR(20),
    IN p_MaPhong INT,
    IN p_MaChucVu INT,
    IN p_TrangThai INT,
    OUT p_Message NVARCHAR(255)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        SET p_Message = N'Lỗi khi cập nhật';
    END;
    
    IF NOT EXISTS (SELECT 1 FROM NhanVien WHERE MaNV = p_MaNV) THEN
        SET p_Message = N'Nhân viên không tồn tại';
    ELSE
        UPDATE NhanVien 
        SET TenNV = p_TenNV, DiaChi = p_DiaChi, SDT = p_SDT, 
            MaPhong = p_MaPhong, MaChucVu = p_MaChucVu, TrangThai = p_TrangThai
        WHERE MaNV = p_MaNV;
        
        SET p_Message = N'Cập nhật thành công';
    END IF;
END$$
DELIMITER ;

-- Procedure: Xóa nhân viên (soft delete - chỉ đổi trạng thái)
DELIMITER $$
CREATE PROCEDURE sp_XoaNhanVien(
    IN p_MaNV INT,
    OUT p_Message NVARCHAR(255)
)
BEGIN
    IF NOT EXISTS (SELECT 1 FROM NhanVien WHERE MaNV = p_MaNV) THEN
        SET p_Message = N'Nhân viên không tồn tại';
    ELSE
        UPDATE NhanVien SET TrangThai = 0 WHERE MaNV = p_MaNV;
        SET p_Message = N'Xóa nhân viên thành công';
    END IF;
END$$
DELIMITER ;

-- =====================================================
-- INDEXES CHO CẢI THIỆN HIỆU NĂNG
-- =====================================================
CREATE INDEX idx_NhanVien_Email ON NhanVien(Email);
CREATE INDEX idx_NhanVien_MaPhong ON NhanVien(MaPhong);
CREATE INDEX idx_NhanVien_TrangThai ON NhanVien(TrangThai);

-- =====================================================
-- GRANTS & PHÂN QUYỀN (tùy chỉnh theo database user)
-- =====================================================

-- =====================================================
-- THIẾT LẬP BẢO MẬT VÀ PHÂN QUYỀN (Yêu cầu 4)
-- =====================================================

-- 1. Xóa user cũ nếu đã tồn tại (để chạy lại script không lỗi)
DROP USER IF EXISTS 'user_nhanvien'@'localhost';
DROP USER IF EXISTS 'user_ketoan'@'localhost';

-- 2. Tạo User mới
CREATE USER 'user_nhanvien'@'localhost' IDENTIFIED BY 'NhanVien@123';
CREATE USER 'user_ketoan'@'localhost' IDENTIFIED BY 'KeToan@456';

-- 3. Phân quyền cho User NHÂN VIÊN
-- Chỉ được SELECT trên DB nhân sự, không thấy DB lương
GRANT SELECT ON DB1_NHANSU.* TO 'user_nhanvien'@'localhost';

-- 4. Phân quyền cho User KẾ TOÁN
-- Được xem nhân sự và quản lý toàn bộ DB lương
GRANT SELECT ON DB1_NHANSU.* TO 'user_ketoan'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON DB2_LUONG.* TO 'user_ketoan'@'localhost';

-- 5. Cấp quyền thực thi các Procedure (Nếu cần)
GRANT EXECUTE ON PROCEDURE DB2_LUONG.sp_TinhLuongThang TO 'user_ketoan'@'localhost';

-- 6. Áp dụng thay đổi
FLUSH PRIVILEGES;

-- Tạo user cho ứng dụng (thay username/password)
-- CREATE USER 'app_user'@'localhost' IDENTIFIED BY 'strong_password';
-- GRANT SELECT, INSERT, UPDATE ON DB1_NHANSU.* TO 'app_user'@'localhost';

COMMIT;
