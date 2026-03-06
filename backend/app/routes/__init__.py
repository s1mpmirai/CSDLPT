from flask import Blueprint

# Import blueprints
from app.routes.auth import auth_bp
from app.routes.nhanvien import nhanvien_bp
from app.routes.luong import luong_bp
from app.routes.phongban import phongban_bp
from app.routes.chucvu import chucvu_bp

__all__ = [
    'auth_bp',
    'nhanvien_bp',
    'luong_bp',
    'phongban_bp',
    'chucvu_bp'
]
