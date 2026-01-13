from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config
from infrastructure.databases.base import Base

# Database configuration for PostgreSQL (Supabase)
DATABASE_URI = Config.DATABASE_URI
engine = create_engine(
    DATABASE_URI,
    pool_pre_ping=True,  # Verify connections before using
    pool_recycle=300,    # Recycle connections after 5 minutes
    echo=False           # Set to True for SQL query logging
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

def init_postgres(app):
    """Initialize PostgreSQL database and create all tables."""
    Base.metadata.create_all(bind=engine)
