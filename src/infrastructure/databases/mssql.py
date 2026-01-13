# Compatibility layer: Re-export PostgreSQL connection as MSSQL for backward compatibility
# All existing imports from infrastructure.databases.mssql will continue to work
# This allows us to switch to PostgreSQL (Supabase) without modifying 42+ files
from infrastructure.databases.postgres import (
    Base,
    session,
    engine,
    SessionLocal
)

def init_mssql(app):
    """Compatibility function - redirects to PostgreSQL initialization."""
    from infrastructure.databases.postgres import init_postgres
    init_postgres(app)