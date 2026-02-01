"""
Notification Service
Handles real-time notifications using Flask-SocketIO
Notifies Owner/Employee when AI creates draft invoices
"""

from flask_socketio import SocketIO, emit, join_room, leave_room
from typing import Dict, Any, Optional
from datetime import datetime


class NotificationService:
    """
    Service for managing real-time notifications
    Uses Socket.IO for WebSocket communication
    """
    
    def __init__(self, socketio: SocketIO):
        self.socketio = socketio
    
    def notify_ai_draft_created(
        self,
        household_id: int,
        invoice_id: int,
        invoice_data: Dict[str, Any],
        confidence: float,
        warnings: list
    ):
        """
        Notify household members when AI creates a draft invoice
        
        Args:
            household_id: Household ID
            invoice_id: Created invoice ID
            invoice_data: Invoice details
            confidence: AI confidence score
            warnings: List of warnings
        """
        notification = {
            'type': 'ai_draft_created',
            'timestamp': datetime.now().isoformat(),
            'data': {
                'invoice_id': invoice_id,
                'invoice': invoice_data,
                'confidence': confidence,
                'warnings': warnings,
                'household_id': household_id
            }
        }
        
        # Emit to household room (all users in same household)
        room = f'household_{household_id}'
        # print(f"DEBUG: Sending notification '{notification['type']}' to room '{room}'")
        self.socketio.emit('notification', notification, room=room)
        # print(f"DEBUG: Notification emitted successfully")
    
    def join_household_room(self, household_id: int):
        """
        Join user to household room for receiving notifications
        
        Args:
            household_id: Household ID to join
        """
        room = f'household_{household_id}'
        join_room(room)
    
    def leave_household_room(self, household_id: int):
        """
        Leave household room
        
        Args:
            household_id: Household ID to leave
        """
        room = f'household_{household_id}'
        leave_room(room)
