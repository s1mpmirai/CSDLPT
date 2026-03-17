"""
Seed demo data for testing
"""
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app import db
from app.models.nhanvien import NhanVien, PhongBan, ChucVu
from app.models.luong import BangLuong, ChiTietLuongThang
from datetime import date, datetime

seed_bp = Blueprint('seed', __name__)

def check_admin():
    """Check if user is admin"""
    claims = get_jwt()
    return claims.get('role') == 'admin'

@seed_bp.route('/employees', methods=['POST'])
@jwt_required()
def seed_employees():
    """Seed demo employees"""
    if not check_admin():
        return jsonify({'success': False, 'message': 'Only admin can seed data'}), 403
    
    try:
        # Make sure departments and positions exist first
        departments = PhongBan.query.all()
        positions = ChucVu.query.all()
        
        if not departments or not positions:
            return jsonify({'success': False, 'message': 'Please seed departments and positions first'}), 400
        
        # Demo employees data
        demo_employees = [
            {
                'tenNV': 'Nguyễn Văn A',
                'ngaySinh': date(1990, 5, 15),
                'gioiTinh': 'Nam',
                'diaChi': '123 Đường ABC, TP HCM',
                'sdt': '0901234567',
                'email': 'nguyenvana@company.com',
                'maPhong': departments[0].MaPhong,
                'maChucVu': positions[1].MaChucVu,
                'ngayVaoLam': date(2020, 1, 15),
            },
            {
                'tenNV': 'Trần Thị B',
                'ngaySinh': date(1992, 8, 20),
                'gioiTinh': 'Nữ',
                'diaChi': '456 Đường DEF, TP HCM',
                'sdt': '0912345678',
                'email': 'tranthib@company.com',
                'maPhong': departments[1].MaPhong,
                'maChucVu': positions[1].MaChucVu,
                'ngayVaoLam': date(2020, 3, 20),
            },
            {
                'tenNV': 'Lê Văn C',
                'ngaySinh': date(1988, 12, 10),
                'gioiTinh': 'Nam',
                'diaChi': '789 Đường GHI, TP HCM',
                'sdt': '0923456789',
                'email': 'levanc@company.com',
                'maPhong': departments[2].MaPhong,
                'maChucVu': positions[1].MaChucVu,
                'ngayVaoLam': date(2019, 6, 10),
            },
            {
                'tenNV': 'Phạm Thị D',
                'ngaySinh': date(1995, 3, 25),
                'gioiTinh': 'Nữ',
                'diaChi': '321 Đường JKL, TP HCM',
                'sdt': '0934567890',
                'email': 'phamthid@company.com',
                'maPhong': departments[3].MaPhong,
                'maChucVu': positions[2].MaChucVu,
                'ngayVaoLam': date(2021, 2, 1),
            },
        ]
        
        count = 0
        for emp_data in demo_employees:
            # Check if employee already exists
            if not NhanVien.query.filter_by(Email=emp_data['email']).first():
                emp = NhanVien(**emp_data, TrangThai=1)
                db.session.add(emp)
                count += 1
        
        db.session.commit()
        return jsonify({'success': True, 'message': f'Seeded {count} employees'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@seed_bp.route('/departments', methods=['POST'])
@jwt_required()
def seed_departments():
    """Seed demo departments"""
    if not check_admin():
        return jsonify({'success': False, 'message': 'Only admin can seed data'}), 403
    
    try:
        demo_departments = [
            {'tenPhong': 'Kỹ Thuật', 'truongPhong': 'Nguyễn Văn A'},
            {'tenPhong': 'Kế Toán', 'truongPhong': 'Trần Thị B'},
            {'tenPhong': 'Nhân Sự', 'truongPhong': 'Lê Văn C'},
            {'tenPhong': 'Marketing', 'truongPhong': 'Phạm Thị D'},
            {'tenPhong': 'Bán Hàng', 'truongPhong': 'Hoàng Văn E'},
        ]
        
        count = 0
        for dept_data in demo_departments:
            if not PhongBan.query.filter_by(TenPhong=dept_data['tenPhong']).first():
                dept = PhongBan(**dept_data)
                db.session.add(dept)
                count += 1
        
        db.session.commit()
        return jsonify({'success': True, 'message': f'Seeded {count} departments'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@seed_bp.route('/positions', methods=['POST'])
@jwt_required()
def seed_positions():
    """Seed demo positions"""
    if not check_admin():
        return jsonify({'success': False, 'message': 'Only admin can seed data'}), 403
    
    try:
        demo_positions = [
            {'tenChucVu': 'Giám đốc'},
            {'tenChucVu': 'Trưởng phòng'},
            {'tenChucVu': 'Nhân viên'},
            {'tenChucVu': 'Thực tập sinh'},
        ]
        
        count = 0
        for pos_data in demo_positions:
            if not ChucVu.query.filter_by(TenChucVu=pos_data['tenChucVu']).first():
                pos = ChucVu(**pos_data)
                db.session.add(pos)
                count += 1
        
        db.session.commit()
        return jsonify({'success': True, 'message': f'Seeded {count} positions'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@seed_bp.route('/payrolls', methods=['POST'])
@jwt_required()
def seed_payrolls():
    """Seed demo payrolls"""
    if not check_admin():
        return jsonify({'success': False, 'message': 'Only admin can seed data'}), 403
    
    try:
        # First seed salary table for employees if not exists
        employees = NhanVien.query.filter_by(TrangThai=1).all()
        
        count = 0
        for emp in employees:
            # Create salary record if not exists
            bang_luong = BangLuong.query.filter_by(MaNV=emp.MaNV).first()
            if not bang_luong:
                bang_luong = BangLuong(
                    MaNV=emp.MaNV,
                    LuongCoBan=10000000,  # 10M base salary
                    HeSoLuong=1.0,
                    PhuCapChucVu=2000000,  # 2M position allowance
                    PhuCapPhongBan=1000000,  # 1M department allowance
                    NgayApDung=date.today(),
                    TrangThai=1
                )
                db.session.add(bang_luong)
            
            # Create payroll details for current month
            now = datetime.now()
            chi_tiet = ChiTietLuongThang.query.filter_by(
                MaNV=emp.MaNV, 
                Thang=now.month, 
                Nam=now.year
            ).first()
            
            if not chi_tiet:
                chi_tiet = ChiTietLuongThang(
                    MaNV=emp.MaNV,
                    Thang=now.month,
                    Nam=now.year,
                    LuongCoBan=10000000,
                    PhuCapChucVu=2000000,
                    PhuCapPhongBan=1000000,
                    TangCa=0,
                    Thuong=0,
                    ThueThanhKhoan=0,
                    BaoHiem=1300000,  # 10% insurance
                    Phat=0,
                    KeoChuyen=0,
                    TrangThai=1,
                    NgayTinhLuong=date.today()
                )
                db.session.add(chi_tiet)
                count += 1
        
        db.session.commit()
        return jsonify({'success': True, 'message': f'Seeded {count} payroll records'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


@seed_bp.route('/all', methods=['POST'])
@jwt_required()
def seed_all():
    """Seed all demo data at once"""
    if not check_admin():
        return jsonify({'success': False, 'message': 'Only admin can seed data'}), 403
    
    results = {
        'departments': 0,
        'positions': 0,
        'employees': 0,
        'payrolls': 0,
    }
    
    try:
        # Seed departments
        demo_depts = [
            {'tenPhong': 'Kỹ Thuật', 'truongPhong': 'Nguyễn Văn A'},
            {'tenPhong': 'Kế Toán', 'truongPhong': 'Trần Thị B'},
            {'tenPhong': 'Nhân Sự', 'truongPhong': 'Lê Văn C'},
            {'tenPhong': 'Marketing', 'truongPhong': 'Phạm Thị D'},
            {'tenPhong': 'Bán Hàng', 'truongPhong': 'Hoàng Văn E'},
        ]
        for dept_data in demo_depts:
            if not PhongBan.query.filter_by(TenPhong=dept_data['tenPhong']).first():
                db.session.add(PhongBan(**dept_data))
                results['departments'] += 1
        
        # Seed positions
        demo_pos = [
            {'tenChucVu': 'Giám đốc'},
            {'tenChucVu': 'Trưởng phòng'},
            {'tenChucVu': 'Nhân viên'},
            {'tenChucVu': 'Thực tập sinh'},
        ]
        for pos_data in demo_pos:
            if not ChucVu.query.filter_by(TenChucVu=pos_data['tenChucVu']).first():
                db.session.add(ChucVu(**pos_data))
                results['positions'] += 1
        
        db.session.commit()
        
        # Seed employees
        departments = PhongBan.query.all()
        positions = ChucVu.query.all()
        
        if departments and positions:
            demo_emps = [
                {
                    'tenNV': 'Nguyễn Văn A',
                    'ngaySinh': date(1990, 5, 15),
                    'gioiTinh': 'Nam',
                    'diaChi': '123 Đường ABC, TP HCM',
                    'sdt': '0901234567',
                    'email': 'nguyenvana@company.com',
                    'maPhong': departments[0].MaPhong,
                    'maChucVu': positions[1].MaChucVu,
                    'ngayVaoLam': date(2020, 1, 15),
                },
                {
                    'tenNV': 'Trần Thị B',
                    'ngaySinh': date(1992, 8, 20),
                    'gioiTinh': 'Nữ',
                    'diaChi': '456 Đường DEF, TP HCM',
                    'sdt': '0912345678',
                    'email': 'tranthib@company.com',
                    'maPhong': departments[1].MaPhong,
                    'maChucVu': positions[1].MaChucVu,
                    'ngayVaoLam': date(2020, 3, 20),
                },
                {
                    'tenNV': 'Lê Văn C',
                    'ngaySinh': date(1988, 12, 10),
                    'gioiTinh': 'Nam',
                    'diaChi': '789 Đường GHI, TP HCM',
                    'sdt': '0923456789',
                    'email': 'levanc@company.com',
                    'maPhong': departments[2].MaPhong,
                    'maChucVu': positions[1].MaChucVu,
                    'ngayVaoLam': date(2019, 6, 10),
                },
                {
                    'tenNV': 'Phạm Thị D',
                    'ngaySinh': date(1995, 3, 25),
                    'gioiTinh': 'Nữ',
                    'diaChi': '321 Đường JKL, TP HCM',
                    'sdt': '0934567890',
                    'email': 'phamthid@company.com',
                    'maPhong': departments[3].MaPhong,
                    'maChucVu': positions[2].MaChucVu,
                    'ngayVaoLam': date(2021, 2, 1),
                },
                {
                    'tenNV': 'Hoàng Văn E',
                    'ngaySinh': date(1993, 7, 30),
                    'gioiTinh': 'Nam',
                    'diaChi': '654 Đường MNO, TP HCM',
                    'sdt': '0945678901',
                    'email': 'hoangvane@company.com',
                    'maPhong': departments[4].MaPhong,
                    'maChucVu': positions[2].MaChucVu,
                    'ngayVaoLam': date(2020, 9, 15),
                },
            ]
            for emp_data in demo_emps:
                if not NhanVien.query.filter_by(Email=emp_data['email']).first():
                    db.session.add(NhanVien(**emp_data, TrangThai=1))
                    results['employees'] += 1
        
        db.session.commit()
        
        # Seed payrolls
        employees = NhanVien.query.filter_by(TrangThai=1).all()
        now = datetime.now()
        
        for emp in employees:
            bang_luong = BangLuong.query.filter_by(MaNV=emp.MaNV).first()
            if not bang_luong:
                db.session.add(BangLuong(
                    MaNV=emp.MaNV,
                    LuongCoBan=10000000,
                    HeSoLuong=1.0,
                    PhuCapChucVu=2000000,
                    PhuCapPhongBan=1000000,
                    NgayApDung=date.today(),
                    TrangThai=1
                ))
            
            chi_tiet = ChiTietLuongThang.query.filter_by(
                MaNV=emp.MaNV,
                Thang=now.month,
                Nam=now.year
            ).first()
            
            if not chi_tiet:
                db.session.add(ChiTietLuongThang(
                    MaNV=emp.MaNV,
                    Thang=now.month,
                    Nam=now.year,
                    LuongCoBan=10000000,
                    PhuCapChucVu=2000000,
                    PhuCapPhongBan=1000000,
                    TangCa=0,
                    Thuong=0,
                    ThueThanhKhoan=0,
                    BaoHiem=1300000,
                    Phat=0,
                    KeoChuyen=0,
                    TrangThai=1,
                    NgayTinhLuong=date.today()
                ))
                results['payrolls'] += 1
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Seeded all demo data',
            'data': results
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
