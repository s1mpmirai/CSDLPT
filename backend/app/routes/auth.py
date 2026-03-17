from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from datetime import datetime, timezone, timedelta
import os

auth_bp = Blueprint('auth', __name__)

# Hardcoded users (nên lưu vào DB trong thực tế)
USERS = {
    'admin': {
        'password': generate_password_hash('admin123'),
        'role': 'admin',
        'name': 'Admin User'
    },
    'ketoan': {
        'password': generate_password_hash('ketoan123'),
        'role': 'ketoan',
        'name': 'Kế toán'
    },
    'nhanvien': {
        'password': generate_password_hash('nhanvien123'),
        'role': 'nhanvien',
        'name': 'Nhân viên',
        'maNV': 4
    }
}

@auth_bp.route('/login', methods=['POST'])
def login():
    """Đăng nhập"""
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'success': False, 'message': 'Missing username or password'}), 400
    
    username = data.get('username')
    password = data.get('password')
    requested_role = data.get('role')
    
    # Kiểm tra user tồn tại
    if username not in USERS:
        return jsonify({'success': False, 'message': 'User not found'}), 404
    
    user = USERS[username]
    
    # Kiểm tra password
    if not check_password_hash(user['password'], password):
        return jsonify({'success': False, 'message': 'Invalid password'}), 401
    
    # Kiểm tra role (nếu frontend gởi lên)
    if requested_role and user['role'] != requested_role:
        return jsonify({'success': False, 'message': f'Tài khoản này không có quyền {requested_role}'}), 403
    
    # Tạo JWT token - identity phải là string
    additional_claims = {'role': user['role']}
    if 'maNV' in user:
        additional_claims['maNV'] = user['maNV']
        
    access_token = create_access_token(
        identity=username,
        additional_claims=additional_claims
    )
    
    return jsonify({
        'success': True,
        'token': access_token,
        'user': {
            'username': username,
            'name': user['name'],
            'role': user['role']
        }
    }), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_user_info():
    """Lấy thông tin user đang đăng nhập"""
    username = get_jwt_identity()  # Lấy username từ 'sub' claim
    claims = get_jwt()  # Lấy tất cả claims
    role = claims.get('role', 'unknown')  # Lấy role từ additional_claims
    
    return jsonify({
        'success': True,
        'user': {
            'username': username,
            'role': role
        }
    }), 200

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Đăng xuất (client xóa token)"""
    return jsonify({
        'success': True,
        'message': 'Logged out successfully'
    }), 200
