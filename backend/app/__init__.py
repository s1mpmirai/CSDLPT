from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import config

db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_name='development'):
    """Application factory"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    
    # Register blueprints
    from app.routes import auth_bp, nhanvien_bp, luong_bp, phongban_bp, chucvu_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(nhanvien_bp, url_prefix='/api/nhanvien')
    app.register_blueprint(luong_bp, url_prefix='/api/luong')
    app.register_blueprint(phongban_bp, url_prefix='/api/phongban')
    app.register_blueprint(chucvu_bp, url_prefix='/api/chucvu')
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    @app.route('/api/health', methods=['GET'])
    def health():
        return {'status': 'OK', 'message': 'Server is running'}, 200
    
    return app
