from datetime import datetime
from app import db

class BangLuong(db.Model):
    """Bảng lương master"""
    __tablename__ = 'BangLuong'
    __bind_key__ = 'db2_luong'
    
    MaBangLuong = db.Column(db.Integer, primary_key=True, autoincrement=True)
    MaNV = db.Column(db.Integer, nullable=False, unique=True)
    LuongCoBan = db.Column(db.Float, nullable=False)
    HeSoLuong = db.Column(db.Float, default=1.0)
    PhuCapChucVu = db.Column(db.Float, default=0)
    PhuCapPhongBan = db.Column(db.Float, default=0)
    NgayApDung = db.Column(db.Date, nullable=False)
    TrangThai = db.Column(db.Integer, default=1)  # 1: Hoạt động, 0: Ngưng
    CreateDate = db.Column(db.DateTime, default=datetime.utcnow)
    UpdateDate = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'maBangLuong': self.MaBangLuong,
            'maNV': self.MaNV,
            'luongCoBan': float(self.LuongCoBan),
            'heSoLuong': float(self.HeSoLuong),
            'phuCapChucVu': float(self.PhuCapChucVu),
            'phuCapPhongBan': float(self.PhuCapPhongBan),
            'ngayApDung': self.NgayApDung.isoformat() if self.NgayApDung else None,
            'trangThai': self.TrangThai
        }

class ChiTietLuongThang(db.Model):
    """Chi tiết lương tháng"""
    __tablename__ = 'ChiTietLuongThang'
    __bind_key__ = 'db2_luong'
    
    MaChiTiet = db.Column(db.Integer, primary_key=True, autoincrement=True)
    MaNV = db.Column(db.Integer, nullable=False)
    Thang = db.Column(db.Integer, nullable=False)
    Nam = db.Column(db.Integer, nullable=False)
    
    # Thành phần lương
    LuongCoBan = db.Column(db.Float, nullable=False)
    PhuCapChucVu = db.Column(db.Float, default=0)
    PhuCapPhongBan = db.Column(db.Float, default=0)
    TangCa = db.Column(db.Float, default=0)
    Thuong = db.Column(db.Float, default=0)
    
    # Các khoản giảm trừ
    ThueThanhKhoan = db.Column(db.Float, default=0)
    BaoHiem = db.Column(db.Float, default=0)
    Phat = db.Column(db.Float, default=0)
    KeoChuyen = db.Column(db.Float, default=0)
    
    TrangThai = db.Column(db.Integer, default=1)
    NgayTinhLuong = db.Column(db.Date)
    GhiChu = db.Column(db.String(255))
    CreateDate = db.Column(db.DateTime, default=datetime.utcnow)
    UpdateDate = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def calculate_luong_thuc_linh(self):
        """Tính lương thực lĩnh"""
        return (self.LuongCoBan + self.PhuCapChucVu + self.PhuCapPhongBan + 
                self.TangCa + self.Thuong - self.ThueThanhKhoan - self.BaoHiem - 
                self.Phat - self.KeoChuyen)
    
    def to_dict(self):
        return {
            'maChiTiet': self.MaChiTiet,
            'maNV': self.MaNV,
            'thang': self.Thang,
            'nam': self.Nam,
            'luongCoBan': float(self.LuongCoBan),
            'phuCapChucVu': float(self.PhuCapChucVu),
            'phuCapPhongBan': float(self.PhuCapPhongBan),
            'tangCa': float(self.TangCa),
            'thuong': float(self.Thuong),
            'thueThanhKhoan': float(self.ThueThanhKhoan),
            'baoHiem': float(self.BaoHiem),
            'phat': float(self.Phat),
            'keoChuyen': float(self.KeoChuyen),
            'luongThucLinh': float(self.calculate_luong_thuc_linh()),
            'trangThai': self.TrangThai,
            'ngayTinhLuong': self.NgayTinhLuong.isoformat() if self.NgayTinhLuong else None,
            'ghiChu': self.GhiChu
        }

class BaoHiemConfig(db.Model):
    """Cấu hình bảo hiểm"""
    __tablename__ = 'BaoHiemConfig'
    __bind_key__ = 'db2_luong'
    
    MaBH = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TenBaoHiem = db.Column(db.String(100), nullable=False)
    TyLeBaoHiem = db.Column(db.Float, nullable=False)
    TyLeNguoiDung = db.Column(db.Float, nullable=False)
    Mota = db.Column(db.String(255))
    TrangThai = db.Column(db.Integer, default=1)
    CreateDate = db.Column(db.DateTime, default=datetime.utcnow)
    UpdateDate = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'maBH': self.MaBH,
            'tenBaoHiem': self.TenBaoHiem,
            'tyLeBaoHiem': float(self.TyLeBaoHiem),
            'tyLeNguoiDung': float(self.TyLeNguoiDung),
            'mota': self.Mota,
            'trangThai': self.TrangThai
        }

class LichSuThayDoiLuong(db.Model):
    """Lịch sử thay đổi lương"""
    __tablename__ = 'LichSuThayDoiLuong'
    __bind_key__ = 'db2_luong'
    
    MaLichSu = db.Column(db.Integer, primary_key=True, autoincrement=True)
    MaNV = db.Column(db.Integer, nullable=False)
    NgayThayDoi = db.Column(db.Date, nullable=False)
    LuongCuBan = db.Column(db.Float)
    LuongMoiBan = db.Column(db.Float)
    LyDo = db.Column(db.String(255))
    NgueNguoi = db.Column(db.String(100))
    CreateDate = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'maLichSu': self.MaLichSu,
            'maNV': self.MaNV,
            'ngayThayDoi': self.NgayThayDoi.isoformat() if self.NgayThayDoi else None,
            'luongCuBan': float(self.LuongCuBan) if self.LuongCuBan else None,
            'luongMoiBan': float(self.LuongMoiBan) if self.LuongMoiBan else None,
            'lyDo': self.LyDo,
            'ngueNguoi': self.NgueNguoi
        }
