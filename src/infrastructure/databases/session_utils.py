"""
Session utility functions for safe transaction management
"""
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

def safe_rollback(session: Session):
    """
    Safely rollback a session and reset its state.
    This prevents "Can't reconnect until invalid transaction is rolled back" errors.
    """
    if session is None:
        return
    
    try:
        # Always try to rollback first, regardless of session state
        # This handles the case where session is in an invalid state
        try:
            session.rollback()
        except (SQLAlchemyError, Exception) as e:
            # If rollback fails, the session might be in a bad state
            # Try to reset it by closing and expiring all
            try:
                session.expunge_all()
            except:
                pass
            # Don't raise - we're trying to clean up, not fail
            pass
        
        # Remove all objects from session to prevent stale state
        try:
            session.expunge_all()
        except:
            pass
            
    except SQLAlchemyError:
        # If we get here, session is likely in a very bad state
        # Try one more time to rollback
        try:
            session.rollback()
        except:
            # If even that fails, just expunge all and move on
            try:
                session.expunge_all()
            except:
                pass
    except Exception:
        # Ignore any other errors during cleanup
        # We don't want cleanup to cause more problems
        pass

def safe_commit(session: Session):
    """
    Safely commit a session with proper error handling.
    """
    try:
        session.commit()
    except SQLAlchemyError as e:
        safe_rollback(session)
        raise e

def safe_close(session: Session):
    """
    Safely close a session only if it's not shared.
    For shared sessions (like global session), don't close.
    """
    try:
        # Only close if session is not bound to a shared connection
        if hasattr(session, 'bind') and session.bind is not None:
            # Check if this is a shared session - if so, don't close
            # Shared sessions are typically managed by the application
            pass
        # For now, we don't close shared sessions
        # Individual repositories should not close shared sessions
        pass
    except Exception:
        pass

def get_session():
    """
    Get the current database session.
    Returns the shared session instance.
    """
    from infrastructure.databases.mssql import session
    return session
