from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models.nhanvien import PhongBan

phongban_bp = Blueprint('phongban', __name__)

@phongban_bp.route('', methods=['GET'])
@jwt_required()
def get_phong_ban_list():
    """Lấy danh sách phòng ban"""
    try:
        phong_ban_list = PhongBan.query.all()
        
        return jsonify({
            'success': True,
            'data': [pb.to_dict() for pb in phong_ban_list]
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@phongban_bp.route('/<int:maPhong>', methods=['GET'])
@jwt_required()
def get_phong_ban_detail(maPhong):
    """Lấy chi tiết phòng ban"""
    try:
        phong_ban = PhongBan.query.get(maPhong)
        
        if not phong_ban:
            return jsonify({'success': False, 'message': 'Phòng ban không tồn tại'}), 404
        
        return jsonify({
            'success': True,
            'data': phong_ban.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@phongban_bp.route('', methods=['POST'])
@jwt_required()
def create_phong_ban():
    """Thêm phòng ban"""
    try:
        data = request.get_json()
        
        if not data.get('tenPhong'):
            return jsonify({'success': False, 'message': 'Missing tenPhong'}), 400
        
        # Kiểm tra tenPhong đã tồn tại
        if PhongBan.query.filter_by(TenPhong=data['tenPhong']).first():
            return jsonify({'success': False, 'message': 'Tên phòng ban đã tồn tại'}), 400
        
        phong_ban = PhongBan(
            TenPhong=data['tenPhong'],
            TruongPhong=data.get('truongPhong')
        )
        
        db.session.add(phong_ban)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Thêm phòng ban thành công',
            'data': phong_ban.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@phongban_bp.route('/<int:maPhong>', methods=['PUT'])
@jwt_required()
def update_phong_ban(maPhong):
    """Cập nhật phòng ban"""
    try:
        phong_ban = PhongBan.query.get(maPhong)
        
        if not phong_ban:
            return jsonify({'success': False, 'message': 'Phòng ban không tồn tại'}), 404
        
        data = request.get_json()
        
        if 'tenPhong' in data:
            phong_ban.TenPhong = data['tenPhong']
        if 'truongPhong' in data:
            phong_ban.TruongPhong = data['truongPhong']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Cập nhật phòng ban thành công',
            'data': phong_ban.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
@phongban_bp.route('/<int:maPhong>', methods=['DELETE'])
@jwt_required()
def delete_phong_ban(maPhong):
    """Xóa phòng ban"""
    try:
        phong_ban = PhongBan.query.get(maPhong)
        
        if not phong_ban:
            return jsonify({'success': False, 'message': 'Phòng ban không tồn tại'}), 404
        
        db.session.delete(phong_ban)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Xóa phòng ban thành công'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
