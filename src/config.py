# Configuration settings for the Flask application
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_default_secret_key'
    DEBUG = os.environ.get('DEBUG', 'False').lower() in ['true', '1']
    TESTING = os.environ.get('TESTING', 'False').lower() in ['true', '1']
    # PostgreSQL connection string for Supabase
    # IMPORTANT: Use Session Pooler for IPv4 compatibility (not Direct connection)
    # Format: postgresql://postgres.[project-ref]:[password]@aws-1-[region].pooler.supabase.com:5432/postgres
    # Project ID: xjghpmiupxldgezcrucj
    # Region: Asia (ap-southeast-2)
    # Connection string from: Dashboard > Connect > Method: Session pooler
    DATABASE_URI = os.environ.get('DATABASE_URI') or \
        'postgresql://postgres.xjghpmiupxldgezcrucj:079206043460@aws-1-ap-southeast-2.pooler.supabase.com:5432/postgres'
    CORS_HEADERS = 'Content-Type'
    
    # Google AI Studio API Configuration
    GOOGLE_AI_API_KEY = os.environ.get('GOOGLE_AI_API_KEY') or ''
    GOOGLE_AI_MODEL = os.environ.get('GOOGLE_AI_MODEL') or 'gemini-1.5-flash'
    GOOGLE_AI_TEMPERATURE = float(os.environ.get('GOOGLE_AI_TEMPERATURE', '0.2'))
    GOOGLE_AI_MAX_TOKENS = int(os.environ.get('GOOGLE_AI_MAX_TOKENS', '2048'))


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    DATABASE_URI = os.environ.get('DATABASE_URI') or \
        'postgresql://postgres.xjghpmiupxldgezcrucj:079206043460@aws-1-ap-southeast-2.pooler.supabase.com:5432/postgres'

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DATABASE_URI = os.environ.get('DATABASE_URI') or \
        'postgresql://postgres.xjghpmiupxldgezcrucj:079206043460@aws-1-ap-southeast-2.pooler.supabase.com:5432/postgres'


class ProductionConfig(Config):
    """Production configuration."""
    DATABASE_URI = os.environ.get('DATABASE_URI') or \
        'postgresql://postgres.xjghpmiupxldgezcrucj:079206043460@aws-1-ap-southeast-2.pooler.supabase.com:5432/postgres'


class SwaggerConfig:
    """Swagger configuration."""
    template = {
        "swagger": "2.0",
        "info": {
            "title": "Todo API",
            "description": "API for managing todos",
            "version": "1.0.0"
        },
        "basePath": "/",
        "schemes": ["http", "https"],
        "consumes": ["application/json"],
        "produces": ["application/json"]
    }

    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": 'apispec',
                "route": '/apispec.json',
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/docs"
    }
