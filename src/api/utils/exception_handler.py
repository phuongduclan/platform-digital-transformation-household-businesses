"""
Helper utilities for handling exceptions with automatic session rollback
"""
from flask import jsonify
from infrastructure.databases.mssql import session
from infrastructure.databases.session_utils import safe_rollback

def handle_exception_with_rollback(error, default_status=500):
    """
    Handle exception and automatically rollback session.
    Returns a Flask JSON response.
    """
    # Always rollback session when there's an exception
    safe_rollback(session)
    
    if isinstance(error, ValueError):
        return jsonify({"error": str(error)}), 400
    else:
        return jsonify({"error": str(error)}), default_status
