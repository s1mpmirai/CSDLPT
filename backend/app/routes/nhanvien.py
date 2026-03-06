from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app import db
from app.models.nhanvien import NhanVien, PhongBan, ChucVu
from sqlalchemy import and_

nhanvien_bp = Blueprint('nhanvien', __name__)

def check_permission(required_role):
    """Kiểm tra quyền"""
    claims = get_jwt()
    user_role = claims.get('role')
    
    if required_role == 'all':
        return True
    
    if required_role == 'admin_ketoan':
        return user_role in ['admin', 'ketoan']
    
    if required_role == 'admin':
        return user_role == 'admin'
    
    return False

@nhanvien_bp.route('', methods=['GET'])
@jwt_required()
def get_nhanvien_list():
    """Lấy danh sách nhân viên"""
    if not check_permission('admin_ketoan'):
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)
        phong_ban = request.args.get('phongBan', None, type=int)
        trang_thai = request.args.get('trangThai', None, type=int)
        
        query = NhanVien.query
        
        # Filter
        if phong_ban:
            query = query.filter_by(MaPhong=phong_ban)
        if trang_thai is not None:
            query = query.filter_by(TrangThai=trang_thai)
        
        # Pagination
        paginated = query.paginate(page=page, per_page=limit)
        
        return jsonify({
            'success': True,
            'data': [nv.to_dict() for nv in paginated.items],
            'total': paginated.total,
            'page': page,
            'pages': paginated.pages
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@nhanvien_bp.route('/<int:maNV>', methods=['GET'])
@jwt_required()
def get_nhanvien_detail(maNV):
    """Lấy chi tiết nhân viên"""
    claims = get_jwt()
    user_role = claims.get('role')
    
    # Nhân viên chỉ xem được thông tin của mình
    if user_role == 'nhanvien':
        identity = get_jwt_identity()
        # Cần mapping username -> maNV (tạm thời cho qua)
        pass
    
    try:
        nhanvien = NhanVien.query.get(maNV)
        
        if not nhanvien:
            return jsonify({'success': False, 'message': 'Nhân viên không tồn tại'}), 404
        
        return jsonify({
            'success': True,
            'data': nhanvien.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@nhanvien_bp.route('', methods=['POST'])
@jwt_required()
def create_nhanvien():
    """Thêm nhân viên mới"""
    if not check_permission('admin'):
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        data = request.get_json()
        
        # Validation
        required_fields = ['tenNV', 'ngaySinh', 'email', 'maPhong', 'maChucVu', 'ngayVaoLam']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'message': f'Missing {field}'}), 400
        
        # Kiểm tra email đã tồn tại
        if NhanVien.query.filter_by(Email=data['email']).first():
            return jsonify({'success': False, 'message': 'Email đã tồn tại'}), 400
        
        # Kiểm tra phòng ban, chức vụ tồn tại
        if not PhongBan.query.get(data['maPhong']):
            return jsonify({'success': False, 'message': 'Phòng ban không tồn tại'}), 400
        if not ChucVu.query.get(data['maChucVu']):
            return jsonify({'success': False, 'message': 'Chức vụ không tồn tại'}), 400
        
        nhanvien = NhanVien(
            TenNV=data['tenNV'],
            NgaySinh=data['ngaySinh'],
            GioiTinh=data.get('gioiTinh'),
            DiaChi=data.get('diaChi'),
            SDT=data.get('sdt'),
            Email=data['email'],
            MaPhong=data['maPhong'],
            MaChucVu=data['maChucVu'],
            NgayVaoLam=data['ngayVaoLam'],
            TrangThai=1
        )
        
        db.session.add(nhanvien)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Thêm nhân viên thành công',
            'data': nhanvien.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@nhanvien_bp.route('/<int:maNV>', methods=['PUT'])
@jwt_required()
def update_nhanvien(maNV):
    """Cập nhật nhân viên"""
    if not check_permission('admin'):
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        nhanvien = NhanVien.query.get(maNV)
        
        if not nhanvien:
            return jsonify({'success': False, 'message': 'Nhân viên không tồn tại'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'tenNV' in data:
            nhanvien.TenNV = data['tenNV']
        if 'ngaySinh' in data:
            nhanvien.NgaySinh = data['ngaySinh']
        if 'gioiTinh' in data:
            nhanvien.GioiTinh = data['gioiTinh']
        if 'diaChi' in data:
            nhanvien.DiaChi = data['diaChi']
        if 'sdt' in data:
            nhanvien.SDT = data['sdt']
        if 'maPhong' in data:
            nhanvien.MaPhong = data['maPhong']
        if 'maChucVu' in data:
            nhanvien.MaChucVu = data['maChucVu']
        if 'trangThai' in data:
            nhanvien.TrangThai = data['trangThai']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Cập nhật nhân viên thành công',
            'data': nhanvien.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@nhanvien_bp.route('/<int:maNV>', methods=['DELETE'])
@jwt_required()
def delete_nhanvien(maNV):
    """Xóa nhân viên (soft delete)"""
    if not check_permission('admin'):
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        nhanvien = NhanVien.query.get(maNV)
        
        if not nhanvien:
            return jsonify({'success': False, 'message': 'Nhân viên không tồn tại'}), 404
        
        nhanvien.TrangThai = 0
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Xóa nhân viên thành công'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
