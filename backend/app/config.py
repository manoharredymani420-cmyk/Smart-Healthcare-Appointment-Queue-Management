import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'medicare-super-secret-production-grade-key-2026')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'medicare-jwt-secret-production-grade-token-key-2026')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 86400)))
    
    # Database configuration
    # Default to sqlite:///medicare.db in project root if DATABASE_URL not set
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if not DATABASE_URL:
        db_path = os.path.join(BASE_DIR, 'medicare.db')
        SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'
    else:
        # Handle postgres:// legacy prefix if present
        if DATABASE_URL.startswith('postgres://'):
            DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
        SQLALCHEMY_DATABASE_URI = DATABASE_URL
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')
    
    # ML Model path
    ML_MODEL_PATH = os.path.join(BASE_DIR, 'ml', 'model.joblib')

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)

class ProductionConfig(Config):
    DEBUG = False

config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
