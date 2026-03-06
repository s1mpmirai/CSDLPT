from datetime import datetime
from app import db

class PhongBan(db.Model):
    """Phòng ban model"""
    __tablename__ = 'PhongBan'
    __bind_key__ = 'db1_nhansu'
    
    MaPhong = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TenPhong = db.Column(db.String(100), nullable=False, unique=True)
    TruongPhong = db.Column(db.String(100))
    CreateDate = db.Column(db.DateTime, default=datetime.utcnow)
    UpdateDate = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    nhanvien = db.relationship('NhanVien', backref='phongban', lazy=True)
    
    def to_dict(self):
        return {
            'maPhong': self.MaPhong,
            'tenPhong': self.TenPhong,
            'truongPhong': self.TruongPhong,
            'createDate': self.CreateDate.isoformat() if self.CreateDate else None
        }

class ChucVu(db.Model):
    """Chức vụ model"""
    __tablename__ = 'ChucVu'
    __bind_key__ = 'db1_nhansu'
    
    MaChucVu = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TenChucVu = db.Column(db.String(100), nullable=False, unique=True)
    CreateDate = db.Column(db.DateTime, default=datetime.utcnow)
    UpdateDate = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    nhanvien = db.relationship('NhanVien', backref='chucvu', lazy=True)
    
    def to_dict(self):
        return {
            'maChucVu': self.MaChucVu,
            'tenChucVu': self.TenChucVu
        }

class NhanVien(db.Model):
    """Nhân viên model"""
    __tablename__ = 'NhanVien'
    __bind_key__ = 'db1_nhansu'
    
    MaNV = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TenNV = db.Column(db.String(100), nullable=False)
    NgaySinh = db.Column(db.Date, nullable=False)
    GioiTinh = db.Column(db.String(10))
    DiaChi = db.Column(db.String(255))
    SDT = db.Column(db.String(20))
    Email = db.Column(db.String(100), nullable=False, unique=True)
    MaPhong = db.Column(db.Integer, db.ForeignKey('PhongBan.MaPhong'), nullable=False)
    MaChucVu = db.Column(db.Integer, db.ForeignKey('ChucVu.MaChucVu'), nullable=False)
    NgayVaoLam = db.Column(db.Date, nullable=False)
    TrangThai = db.Column(db.Integer, default=1)  # 1: Đang làm, 0: Nghỉ việc
    CreateDate = db.Column(db.DateTime, default=datetime.utcnow)
    UpdateDate = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'maNV': self.MaNV,
            'tenNV': self.TenNV,
            'ngaySinh': self.NgaySinh.isoformat() if self.NgaySinh else None,
            'gioiTinh': self.GioiTinh,
            'diaChi': self.DiaChi,
            'sdt': self.SDT,
            'email': self.Email,
            'maPhong': self.MaPhong,
            'tenPhong': self.phongban.TenPhong if self.phongban else None,
            'maChucVu': self.MaChucVu,
            'tenChucVu': self.chucvu.TenChucVu if self.chucvu else None,
            'ngayVaoLam': self.NgayVaoLam.isoformat() if self.NgayVaoLam else None,
            'trangThai': self.TrangThai,
            'createDate': self.CreateDate.isoformat() if self.CreateDate else None
        }
