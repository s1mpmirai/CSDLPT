from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models.nhanvien import ChucVu

chucvu_bp = Blueprint('chucvu', __name__)

@chucvu_bp.route('', methods=['GET'])
@jwt_required()
def get_chuc_vu_list():
    """Lấy danh sách chức vụ"""
    try:
        chuc_vu_list = ChucVu.query.all()
        
        return jsonify({
            'success': True,
            'data': [cv.to_dict() for cv in chuc_vu_list]
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@chucvu_bp.route('/<int:maChucVu>', methods=['GET'])
@jwt_required()
def get_chuc_vu_detail(maChucVu):
    """Lấy chi tiết chức vụ"""
    try:
        chuc_vu = ChucVu.query.get(maChucVu)
        
        if not chuc_vu:
            return jsonify({'success': False, 'message': 'Chức vụ không tồn tại'}), 404
        
        return jsonify({
            'success': True,
            'data': chuc_vu.to_dict()
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@chucvu_bp.route('', methods=['POST'])
@jwt_required()
def create_chuc_vu():
    """Thêm chức vụ"""
    try:
        data = request.get_json()
        
        if not data.get('tenChucVu'):
            return jsonify({'success': False, 'message': 'Missing tenChucVu'}), 400
        
        # Kiểm tra tenChucVu đã tồn tại
        if ChucVu.query.filter_by(TenChucVu=data['tenChucVu']).first():
            return jsonify({'success': False, 'message': 'Chức vụ đã tồn tại'}), 400
        
        chuc_vu = ChucVu(TenChucVu=data['tenChucVu'])
        
        db.session.add(chuc_vu)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Thêm chức vụ thành công',
            'data': chuc_vu.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
@chucvu_bp.route('/<int:maChucVu>', methods=['PUT'])
@jwt_required()
def update_chuc_vu(maChucVu):
    """Cập nhật chức vụ"""
    try:
        chuc_vu = ChucVu.query.get(maChucVu)
        
        if not chuc_vu:
            return jsonify({'success': False, 'message': 'Chức vụ không tồn tại'}), 404
        
        data = request.get_json()
        
        if 'tenChucVu' in data:
            chuc_vu.TenChucVu = data['tenChucVu']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Cập nhật chức vụ thành công',
            'data': chuc_vu.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@chucvu_bp.route('/<int:maChucVu>', methods=['DELETE'])
@jwt_required()
def delete_chuc_vu(maChucVu):
    """Xóa chức vụ"""
    try:
        chuc_vu = ChucVu.query.get(maChucVu)
        
        if not chuc_vu:
            return jsonify({'success': False, 'message': 'Chức vụ không tồn tại'}), 404
        
        db.session.delete(chuc_vu)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Xóa chức vụ thành công'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
