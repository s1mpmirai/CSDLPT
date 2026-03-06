-- =====================================================
-- DATABASE 2: DB2_LUONG
-- Chứa thông tin Lương, Bảo hiểm, Chi tiết lương
-- =====================================================

DROP DATABASE IF EXISTS DB2_LUONG;
CREATE DATABASE DB2_LUONG;
USE DB2_LUONG;

-- =====================================================
-- 1. BẢNG BẢNG LƯƠNG (Master)
-- =====================================================
CREATE TABLE BangLuong (
    MaBangLuong INT PRIMARY KEY AUTO_INCREMENT,
    MaNV INT NOT NULL UNIQUE, -- Reference từ DB1
    LuongCoBan DECIMAL(12, 2) NOT NULL CHECK (LuongCoBan > 0),
    HeSoLuong FLOAT DEFAULT 1.0 CHECK (HeSoLuong > 0),
    PhuCapChucVu DECIMAL(12, 2) DEFAULT 0,
    PhuCapPhongBan DECIMAL(12, 2) DEFAULT 0,
    NgayApDung DATE NOT NULL,
    TrangThai INT DEFAULT 1 CHECK (TrangThai IN (0, 1)), -- 1: Hoạt động, 0: Ngưng
    CreateDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    UpdateDate DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_MaNV (MaNV),
    INDEX idx_NgayApDung (NgayApDung),
    INDEX idx_TrangThai (TrangThai)
);

-- =====================================================
-- 2. BẢNG CHI TIẾT LƯƠNG THÁNG
-- =====================================================
CREATE TABLE ChiTietLuongThang (
    MaChiTiet INT PRIMARY KEY AUTO_INCREMENT,
    MaNV INT NOT NULL,
    Thang INT NOT NULL CHECK (Thang BETWEEN 1 AND 12),
    Nam INT NOT NULL CHECK (Nam >= 2020),
    
    -- Thành phần lương
    LuongCoBan DECIMAL(12, 2) NOT NULL,
    PhuCapChucVu DECIMAL(12, 2) DEFAULT 0,
    PhuCapPhongBan DECIMAL(12, 2) DEFAULT 0,
    TangCa DECIMAL(12, 2) DEFAULT 0,
    Thuong DECIMAL(12, 2) DEFAULT 0,
    
    -- Các khoản giảm trừ
    ThueThanhKhoan DECIMAL(12, 2) DEFAULT 0,
    BaoHiem DECIMAL(12, 2) DEFAULT 0, -- BHXH + BHYT + BHTN
    Phat DECIMAL(12, 2) DEFAULT 0,
    KeoChuyen DECIMAL(12, 2) DEFAULT 0, -- Khoản khác
    
    -- Lương thực lĩnh
    LuongThucLinh DECIMAL(12, 2) GENERATED ALWAYS AS (
        LuongCoBan + PhuCapChucVu + PhuCapPhongBan + TangCa + Thuong 
        - ThueThanhKhoan - BaoHiem - Phat - KeoChuyen
    ) STORED,
    
    TrangThai INT DEFAULT 1 CHECK (TrangThai IN (0, 1)), -- 1: Đã tính, 0: Nháp
    NgayTinhLuong DATE,
    GhiChu NVARCHAR(255),
    CreateDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    UpdateDate DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    UNIQUE KEY unique_MaNV_Thang_Nam (MaNV, Thang, Nam),
    INDEX idx_MaNV (MaNV),
    INDEX idx_ThangNam (Thang, Nam),
    INDEX idx_NgayTinhLuong (NgayTinhLuong),
    INDEX idx_TrangThai (TrangThai)
);

-- =====================================================
-- 3. BẢNG BẢNG BẢOHIỂM (Tỉ lệ bảo hiểm)
-- =====================================================
CREATE TABLE BaoHiemConfig (
    MaBH INT PRIMARY KEY AUTO_INCREMENT,
    TenBaoHiem NVARCHAR(100) NOT NULL,
    TyLeBaoHiem FLOAT NOT NULL CHECK (TyLeBaoHiem >= 0),
    TyLeNguoiDung FLOAT NOT NULL CHECK (TyLeNguoiDung >= 0),
    Mota NVARCHAR(255),
    TrangThai INT DEFAULT 1,
    CreateDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    UpdateDate DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- =====================================================
-- 4. BẢNG TẮC CÃO (Thay đổi lương)
-- =====================================================
CREATE TABLE LichSuThayDoiLuong (
    MaLichSu INT PRIMARY KEY AUTO_INCREMENT,
    MaNV INT NOT NULL,
    NgayThayDoi DATE NOT NULL,
    LuongCuBan DECIMAL(12, 2),
    LuongMoiBan DECIMAL(12, 2),
    LyDo NVARCHAR(255),
    NgueNguoi NVARCHAR(100),
    CreateDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_MaNV (MaNV),
    INDEX idx_NgayThayDoi (NgayThayDoi)
);

-- =====================================================
-- 5. BẢNG HỢP ĐỒNG LƯƠNG (Tùy chọn)
-- =====================================================
CREATE TABLE HopDongLuong (
    MaHopDong INT PRIMARY KEY AUTO_INCREMENT,
    MaNV INT NOT NULL UNIQUE,
    NgayKyHopDong DATE NOT NULL,
    NgayHetHan DATE,
    LuongKhiBatDau DECIMAL(12, 2),
    LuongHienTai DECIMAL(12, 2),
    SoTienTangHangNam DECIMAL(12, 2),
    TrangThai INT DEFAULT 1, -- 1: Hoạt động, 0: Hết hạn
    GhiChu NVARCHAR(255),
    CreateDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    UpdateDate DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_MaNV (MaNV),
    INDEX idx_TrangThai (TrangThai)
);

-- =====================================================
-- SEED DATA CHO DB2
-- =====================================================

-- Thêm cấu hình bảo hiểm
INSERT INTO BaoHiemConfig (TenBaoHiem, TyLeBaoHiem, TyLeNguoiDung, Mota) VALUES
(N'Bảo hiểm xã hội', 17.5, 8, N'BHXH - Tỉ lệ chung'),
(N'Bảo hiểm y tế', 3, 1.5, N'BHYT - Tỉ lệ chung'),
(N'Bảo hiểm thất nghiệp', 1, 0.5, N'BHTN - Tỉ lệ chung');

-- Thêm bảng lương cho nhân viên (tương ứng với 8 nhân viên trong DB1)
INSERT INTO BangLuong (MaNV, LuongCoBan, HeSoLuong, PhuCapChucVu, PhuCapPhongBan, NgayApDung, TrangThai) VALUES
(1, 5000000, 1.0, 500000, 300000, '2020-01-15', 1),
(2, 5000000, 1.0, 500000, 300000, '2020-03-20', 1),
(3, 5000000, 1.0, 500000, 300000, '2019-06-10', 1),
(4, 3500000, 1.0, 200000, 300000, '2021-02-01', 1),
(5, 3500000, 1.0, 200000, 300000, '2020-09-15', 1),
(6, 3500000, 1.0, 200000, 300000, '2021-04-10', 1),
(7, 3500000, 1.0, 200000, 300000, '2022-01-20', 1),
(8, 3500000, 1.0, 200000, 300000, '2022-06-15', 1);

-- Thêm chi tiết lương tháng 2/2026 (ví dụ)
INSERT INTO ChiTietLuongThang (MaNV, Thang, Nam, LuongCoBan, PhuCapChucVu, PhuCapPhongBan, TangCa, Thuong, ThueThanhKhoan, BaoHiem, Phat, KeoChuyen, TrangThai, NgayTinhLuong) VALUES
(1, 2, 2026, 5000000, 500000, 300000, 300000, 0, 0, 450000, 0, 0, 1, '2026-03-01'),
(2, 2, 2026, 5000000, 500000, 300000, 250000, 0, 0, 450000, 0, 0, 1, '2026-03-01'),
(3, 2, 2026, 5000000, 500000, 300000, 0, 0, 0, 450000, 0, 0, 1, '2026-03-01'),
(4, 2, 2026, 3500000, 200000, 300000, 100000, 0, 0, 300000, 0, 0, 1, '2026-03-01'),
(5, 2, 2026, 3500000, 200000, 300000, 150000, 0, 0, 300000, 0, 0, 1, '2026-03-01'),
(6, 2, 2026, 3500000, 200000, 300000, 0, 0, 0, 300000, 0, 0, 1, '2026-03-01'),
(7, 2, 2026, 3500000, 200000, 300000, 50000, 0, 0, 300000, 0, 0, 1, '2026-03-01'),
(8, 2, 2026, 3500000, 200000, 300000, 0, 0, 0, 300000, 0, 0, 1, '2026-03-01');

-- =====================================================
-- VIEWS CHO DB2
-- =====================================================

-- View: Lương tháng chi tiết
CREATE VIEW vw_LuongThangChiTiet AS
SELECT 
    ct.MaChiTiet,
    ct.MaNV,
    ct.Thang,
    ct.Nam,
    ct.LuongCoBan,
    ct.PhuCapChucVu,
    ct.PhuCapPhongBan,
    ct.TangCa,
    ct.Thuong,
    ct.ThueThanhKhoan,
    ct.BaoHiem,
    ct.Phat,
    ct.KeoChuyen,
    ct.LuongThucLinh,
    ct.TrangThai,
    ct.NgayTinhLuong
FROM ChiTietLuongThang ct
WHERE ct.TrangThai = 1;

-- View: Tổng hợp lương theo tháng
CREATE VIEW vw_TongHopLuongThang AS
SELECT 
    Thang,
    Nam,
    COUNT(DISTINCT MaNV) AS SoNhanVien,
    SUM(LuongCoBan) AS TongLuongCoBan,
    SUM(PhuCapChucVu) AS TongPhuCapChucVu,
    SUM(PhuCapPhongBan) AS TongPhuCapPhongBan,
    SUM(TangCa) AS TongTangCa,
    SUM(Thuong) AS TongThuong,
    SUM(ThueThanhKhoan) AS TongThueThanhKhoan,
    SUM(BaoHiem) AS TongBaoHiem,
    SUM(Phat) AS TongPhat,
    SUM(LuongThucLinh) AS TongLuongThucLinh,
    MAX(NgayTinhLuong) AS NgayTinhLuong
FROM ChiTietLuongThang
WHERE TrangThai = 1
GROUP BY Thang, Nam;

-- =====================================================
-- STORED PROCEDURES CHO DB2
-- =====================================================

-- Procedure: Thêm/Cập nhật bảng lương
DELIMITER $$
CREATE PROCEDURE sp_CapNhatBangLuong(
    IN p_MaNV INT,
    IN p_LuongCoBan DECIMAL(12, 2),
    IN p_HeSoLuong FLOAT,
    IN p_PhuCapChucVu DECIMAL(12, 2),
    IN p_PhuCapPhongBan DECIMAL(12, 2),
    IN p_NgayApDung DATE,
    OUT p_Message NVARCHAR(255)
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        SET p_Message = N'Lỗi khi cập nhật bảng lương';
    END;
    
    IF EXISTS (SELECT 1 FROM BangLuong WHERE MaNV = p_MaNV) THEN
        UPDATE BangLuong 
        SET LuongCoBan = p_LuongCoBan,
            HeSoLuong = p_HeSoLuong,
            PhuCapChucVu = p_PhuCapChucVu,
            PhuCapPhongBan = p_PhuCapPhongBan,
            NgayApDung = p_NgayApDung
        WHERE MaNV = p_MaNV;
        SET p_Message = N'Cập nhật bảng lương thành công';
    ELSE
        INSERT INTO BangLuong (MaNV, LuongCoBan, HeSoLuong, PhuCapChucVu, PhuCapPhongBan, NgayApDung, TrangThai)
        VALUES (p_MaNV, p_LuongCoBan, p_HeSoLuong, p_PhuCapChucVu, p_PhuCapPhongBan, p_NgayApDung, 1);
        SET p_Message = N'Thêm bảng lương thành công';
    END IF;
END$$
DELIMITER ;

-- Procedure: Tính lương tháng cho 1 nhân viên
DELIMITER $$
CREATE PROCEDURE sp_TinhLuongThang(
    IN p_MaNV INT,
    IN p_Thang INT,
    IN p_Nam INT,
    OUT p_Message NVARCHAR(255)
)
BEGIN
    DECLARE v_LuongCoBan DECIMAL(12, 2);
    DECLARE v_PhuCapChucVu DECIMAL(12, 2);
    DECLARE v_PhuCapPhongBan DECIMAL(12, 2);
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        SET p_Message = N'Lỗi khi tính lương';
    END;
    
    -- Lấy thông tin lương từ bảng lương
    SELECT LuongCoBan, PhuCapChucVu, PhuCapPhongBan 
    INTO v_LuongCoBan, v_PhuCapChucVu, v_PhuCapPhongBan
    FROM BangLuong
    WHERE MaNV = p_MaNV AND TrangThai = 1;
    
    IF v_LuongCoBan IS NULL THEN
        SET p_Message = N'Nhân viên không có bảng lương';
    ELSE
        -- Kiểm tra xem tháng năm đã tính chưa
        IF EXISTS (SELECT 1 FROM ChiTietLuongThang WHERE MaNV = p_MaNV AND Thang = p_Thang AND Nam = p_Nam) THEN
            SET p_Message = N'Lương tháng này đã được tính';
        ELSE
            -- Thêm chi tiết lương
            INSERT INTO ChiTietLuongThang (MaNV, Thang, Nam, LuongCoBan, PhuCapChucVu, PhuCapPhongBan, BaoHiem, TrangThai, NgayTinhLuong)
            VALUES (p_MaNV, p_Thang, p_Nam, v_LuongCoBan, v_PhuCapChucVu, v_PhuCapPhongBan, 
                    ROUND((v_LuongCoBan + v_PhuCapChucVu + v_PhuCapPhongBan) * 0.1, 0), 
                    1, CURDATE());
            SET p_Message = N'Tính lương thành công';
        END IF;
    END IF;
END$$
DELIMITER ;

-- Procedure: Tính lương cho tất cả nhân viên
DELIMITER $$
CREATE PROCEDURE sp_TinhLuongToanBoThang(
    IN p_Thang INT,
    IN p_Nam INT,
    OUT p_SoNhanVienTinh INT,
    OUT p_Message NVARCHAR(255)
)
BEGIN
    DECLARE v_Done INT DEFAULT FALSE;
    DECLARE v_MaNV INT;
    DECLARE cur CURSOR FOR 
        SELECT MaNV FROM BangLuong WHERE TrangThai = 1;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET v_Done = TRUE;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        SET p_Message = N'Lỗi khi tính lương tổng';
        SET p_SoNhanVienTinh = 0;
    END;
    
    SET p_SoNhanVienTinh = 0;
    OPEN cur;
    
    read_loop: LOOP
        FETCH cur INTO v_MaNV;
        IF v_Done THEN
            LEAVE read_loop;
        END IF;
        
        IF NOT EXISTS (SELECT 1 FROM ChiTietLuongThang WHERE MaNV = v_MaNV AND Thang = p_Thang AND Nam = p_Nam) THEN
            CALL sp_TinhLuongThang(v_MaNV, p_Thang, p_Nam, @tmp_msg);
            SET p_SoNhanVienTinh = p_SoNhanVienTinh + 1;
        END IF;
    END LOOP;
    
    CLOSE cur;
    SET p_Message = CONCAT(N'Đã tính lương cho ', p_SoNhanVienTinh, N' nhân viên');
END$$
DELIMITER ;

-- =====================================================
-- INDEXES
-- =====================================================
CREATE INDEX idx_BangLuong_MaNV ON BangLuong(MaNV);
CREATE INDEX idx_BangLuong_NgayApDung ON BangLuong(NgayApDung);
CREATE INDEX idx_ChiTietLuong_MaNV_ThangNam ON ChiTietLuongThang(MaNV, Thang, Nam);
CREATE INDEX idx_ChiTietLuong_NgayTinh ON ChiTietLuongThang(NgayTinhLuong);

COMMIT;
