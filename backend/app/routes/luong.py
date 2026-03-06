from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app import db
from app.models.luong import BangLuong, ChiTietLuongThang
from datetime import date

luong_bp = Blueprint('luong', __name__)

def check_permission(required_role):
    """Kiểm tra quyền"""
    claims = get_jwt()
    user_role = claims.get('role')
    
    if required_role == 'admin_ketoan':
        return user_role in ['admin', 'ketoan']
    if required_role == 'admin':
        return user_role == 'admin'
    
    return False

@luong_bp.route('/<int:maNV>', methods=['GET'])
@jwt_required()
def get_bang_luong(maNV):
    """Lấy bảng lương của nhân viên"""
    try:
        bang_luong = BangLuong.query.filter_by(MaNV=maNV).first()
        
        if not bang_luong:
            return jsonify({'success': False, 'message': 'Bảng lương không tồn tại'}), 404
        
        return jsonify({
            'success': True,
            'data': bang_luong.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@luong_bp.route('/<int:maNV>', methods=['PUT'])
@jwt_required()
def update_bang_luong(maNV):
    """Cập nhật bảng lương"""
    if not check_permission('admin_ketoan'):
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        data = request.get_json()
        bang_luong = BangLuong.query.filter_by(MaNV=maNV).first()
        
        if not bang_luong:
            # Tạo bảng lương mới
            bang_luong = BangLuong(
                MaNV=maNV,
                LuongCoBan=data.get('luongCoBan', 0),
                HeSoLuong=data.get('heSoLuong', 1.0),
                PhuCapChucVu=data.get('phuCapChucVu', 0),
                PhuCapPhongBan=data.get('phuCapPhongBan', 0),
                NgayApDung=data.get('ngayApDung', date.today()),
                TrangThai=1
            )
            db.session.add(bang_luong)
        else:
            # Cập nhật bảng lương hiện tại
            if 'luongCoBan' in data:
                bang_luong.LuongCoBan = data['luongCoBan']
            if 'heSoLuong' in data:
                bang_luong.HeSoLuong = data['heSoLuong']
            if 'phuCapChucVu' in data:
                bang_luong.PhuCapChucVu = data['phuCapChucVu']
            if 'phuCapPhongBan' in data:
                bang_luong.PhuCapPhongBan = data['phuCapPhongBan']
            if 'ngayApDung' in data:
                bang_luong.NgayApDung = data['ngayApDung']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Cập nhật bảng lương thành công',
            'data': bang_luong.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@luong_bp.route('/chi-tiet/<int:maNV>', methods=['GET'])
@jwt_required()
def get_chi_tiet_luong(maNV):
    """Lấy chi tiết lương tháng"""
    try:
        thang = request.args.get('thang', type=int)
        nam = request.args.get('nam', type=int)
        
        if not thang or not nam:
            return jsonify({'success': False, 'message': 'Missing thang or nam'}), 400
        
        chi_tiet = ChiTietLuongThang.query.filter_by(
            MaNV=maNV, Thang=thang, Nam=nam
        ).first()
        
        if not chi_tiet:
            return jsonify({'success': False, 'message': 'Chi tiết lương không tồn tại'}), 404
        
        return jsonify({
            'success': True,
            'data': chi_tiet.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@luong_bp.route('/chi-tiet', methods=['POST'])
@jwt_required()
def create_chi_tiet_luong():
    """Tính lương tháng"""
    if not check_permission('admin_ketoan'):
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        data = request.get_json()
        
        # Kiểm tra tháng năm
        if not data.get('thang') or not data.get('nam'):
            return jsonify({'success': False, 'message': 'Missing thang or nam'}), 400
        
        # Nếu maNV không có -> tính cho tất cả
        maNV = data.get('maNV')
        
        if maNV:
            # Tính cho 1 nhân viên
            bang_luong = BangLuong.query.filter_by(MaNV=maNV, TrangThai=1).first()
            if not bang_luong:
                return jsonify({'success': False, 'message': 'Bảng lương không tồn tại'}), 404
            
            # Kiểm tra đã tính
            existing = ChiTietLuongThang.query.filter_by(
                MaNV=maNV, Thang=data['thang'], Nam=data['nam']
            ).first()
            if existing:
                return jsonify({'success': False, 'message': 'Lương tháng này đã được tính'}), 400
            
            # Tạo chi tiết lương
            chi_tiet = ChiTietLuongThang(
                MaNV=maNV,
                Thang=data['thang'],
                Nam=data['nam'],
                LuongCoBan=bang_luong.LuongCoBan,
                PhuCapChucVu=bang_luong.PhuCapChucVu,
                PhuCapPhongBan=bang_luong.PhuCapPhongBan,
                BaoHiem=round((bang_luong.LuongCoBan + bang_luong.PhuCapChucVu + bang_luong.PhuCapPhongBan) * 0.1, 0),
                TrangThai=1,
                NgayTinhLuong=date.today()
            )
            db.session.add(chi_tiet)
        else:
            # Tính cho tất cả nhân viên
            bang_luong_list = BangLuong.query.filter_by(TrangThai=1).all()
            count = 0
            
            for bang_luong in bang_luong_list:
                existing = ChiTietLuongThang.query.filter_by(
                    MaNV=bang_luong.MaNV, Thang=data['thang'], Nam=data['nam']
                ).first()
                
                if not existing:
                    chi_tiet = ChiTietLuongThang(
                        MaNV=bang_luong.MaNV,
                        Thang=data['thang'],
                        Nam=data['nam'],
                        LuongCoBan=bang_luong.LuongCoBan,
                        PhuCapChucVu=bang_luong.PhuCapChucVu,
                        PhuCapPhongBan=bang_luong.PhuCapPhongBan,
                        BaoHiem=round((bang_luong.LuongCoBan + bang_luong.PhuCapChucVu + bang_luong.PhuCapPhongBan) * 0.1, 0),
                        TrangThai=1,
                        NgayTinhLuong=date.today()
                    )
                    db.session.add(chi_tiet)
                    count += 1
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Tính lương thành công'
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@luong_bp.route('/danh-sach', methods=['GET'])
@jwt_required()
def get_danh_sach_luong_thang():
    """Lấy danh sách lương tháng"""
    if not check_permission('admin_ketoan'):
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        thang = request.args.get('thang', type=int)
        nam = request.args.get('nam', type=int)
        
        if not thang or not nam:
            return jsonify({'success': False, 'message': 'Missing thang or nam'}), 400
        
        chi_tiet_list = ChiTietLuongThang.query.filter_by(
            Thang=thang, Nam=nam, TrangThai=1
        ).all()
        
        return jsonify({
            'success': True,
            'data': [ct.to_dict() for ct in chi_tiet_list]
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
