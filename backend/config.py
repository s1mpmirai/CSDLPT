import os
from datetime import timedelta, timezone
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev_secret_key_change_in_production')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt_secret_key_change_in_production')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    
    # JWT Configuration - Use UTC for consistent timestamp handling
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    JWT_ALGORITHM = 'HS256'
    JWT_VERIFY_EXP = True  # Verify expiration
    JWT_DECODE_LEEWAY = 10  # Allow 10 seconds leeway for clock skew

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    
    # Default database (dùng DB1)
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL_DB1',
        'mysql+pymysql://app_user:app_secure_password_123@localhost/DB1_NHANSU'
    )
    
    # DB1 - Nhân sự & DB2 - Lương
    SQLALCHEMY_BINDS = {
        'db1_nhansu': os.getenv(
            'DATABASE_URL_DB1',
            'mysql+pymysql://app_user:app_secure_password_123@localhost/DB1_NHANSU'
        ),
        'db2_luong': os.getenv(
            'DATABASE_URL_DB2',
            'mysql+pymysql://app_user:app_secure_password_123@localhost/DB2_LUONG'
        )
    }

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    
    # Default database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL_DB1')
    
    SQLALCHEMY_BINDS = {
        'db1_nhansu': os.getenv('DATABASE_URL_DB1'),
        'db2_luong': os.getenv('DATABASE_URL_DB2')
    }

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
