"""
AI Invoice Controller
API endpoints for AI-powered invoice creation from natural language
"""

from flask import Blueprint, request, jsonify
from services.ai_invoice_service import AIInvoiceService
from external_services.google_ai_client import GoogleAIClient
from services.invoice_service import InvoiceService
from services.product_service import ProductService
from services.customer_service import CustomerService
from services.unit_service import UnitService
from services.invoice_detail_service import InvoiceDetailService

from infrastructure.repositories.invoice_repository import InvoiceRepository
from infrastructure.repositories.invoice_detail_repository import InvoiceDetailRepository
from infrastructure.repositories.product_repository import ProductRepository
from infrastructure.repositories.customer_repository import CustomerRepository
from infrastructure.repositories.unit_repository import UnitRepository

from api.utils.auth_utils import token_required, get_household_id_from_token
from config import Config
from infrastructure.databases.session_utils import get_session
from datetime import datetime


# Blueprint for Owner
owner_ai_invoice_bp = Blueprint(
    'owner_ai_invoices',
    __name__,
    url_prefix='/api/owner/ai-invoices'
)

# Blueprint for Employee
employee_ai_invoice_bp = Blueprint(
    'employee_ai_invoices',
    __name__,
    url_prefix='/api/employee/ai-invoices'
)


def get_ai_invoice_service():
    """
    Initialize AIInvoiceService with dependencies
    """
    session = get_session()
    
    # Initialize AI client
    ai_client = GoogleAIClient(
        api_key=Config.GOOGLE_AI_API_KEY,
        model=Config.GOOGLE_AI_MODEL
    )
    
    # Initialize repositories
    invoice_repository = InvoiceRepository()
    invoice_detail_repository = InvoiceDetailRepository()
    product_repository = ProductRepository()
    customer_repository = CustomerRepository()
    unit_repository = UnitRepository()
    
    # Set session for repositories
    invoice_repository.session = session
    invoice_detail_repository.session = session
    product_repository.session = session
    customer_repository.session = session
    unit_repository.session = session
    
    # Initialize services
    invoice_detail_service = InvoiceDetailService(invoice_detail_repository, invoice_repository)
    invoice_service = InvoiceService(invoice_repository, invoice_detail_repository)
    product_service = ProductService(product_repository)
    customer_service = CustomerService(customer_repository)
    unit_service = UnitService(unit_repository)
    
    # Initialize AI Invoice Service
    return AIInvoiceService(
        ai_client=ai_client,
        invoice_service=invoice_service,
        product_service=product_service,
        customer_service=customer_service,
        unit_service=unit_service
    )


def invoice_to_dict(invoice):
    """Convert Invoice object to dict"""
    try:
        # Get details - fetch them if not loaded
        details = []
        if hasattr(invoice, 'details') and invoice.details:
            for detail in invoice.details:
                try:
                    detail_dict = {
                        'id': detail.id,
                        'product_id': detail.product_id,
                        'unit_id': detail.unit_id,
                        'quantity': detail.quantity,
                        'price': float(detail.price) if detail.price is not None else 0,
                        'vat': detail.vat,
                        'discount': detail.discount,
                        'description': detail.description,
                        'status': detail.status,
                        'created_at': detail.created_at.isoformat() if detail.created_at else None,
                        'updated_at': detail.updated_at.isoformat() if detail.updated_at else None
                    }
                    details.append(detail_dict)
                except AttributeError as e:
                    # Skip details with missing attributes
                    print(f"Warning: Skipping detail due to missing attribute: {str(e)}")
                    continue
        else:
            # If details are not loaded, try to fetch them from the repository
            try:
                session = getattr(invoice, 'session', None)
                if session and hasattr(invoice, 'id'):
                    from infrastructure.repositories.invoice_detail_repository import InvoiceDetailRepository
                    detail_repo = InvoiceDetailRepository()
                    detail_repo.session = session
                    invoice_details = detail_repo.list_by_invoice_id(invoice.id)
                    for detail in invoice_details:
                        details.append({
                            'id': detail.id,
                            'product_id': detail.product_id,
                            'unit_id': detail.unit_id,
                            'quantity': detail.quantity,
                            'price': float(detail.price) if detail.price is not None else 0,
                            'vat': detail.vat,
                            'discount': detail.discount,
                            'description': detail.description,
                            'status': detail.status,
                            'created_at': detail.created_at.isoformat() if detail.created_at else None,
                            'updated_at': detail.updated_at.isoformat() if detail.updated_at else None
                        })
            except Exception as fetch_error:
                print(f"Warning: Could not fetch invoice details: {str(fetch_error)}")
        
        return {
            'id': invoice.id,
            'household_id': invoice.household_id,
            'seller_id': invoice.seller_id,
            'customer_id': invoice.customer_id,
            'invoice_type': invoice.invoice_type,
            'discount_total': float(invoice.discount_total) if invoice.discount_total else 0,
            'vat_total': float(invoice.vat_total) if invoice.vat_total else 0,
            'total_amount': float(invoice.total_amount) if invoice.total_amount else 0,
            'description': invoice.description,
            'status': invoice.status,
            'created_by': invoice.created_by,
            'updated_by': invoice.updated_by,
            'created_at': invoice.created_at.isoformat() if invoice.created_at else None,
            'updated_at': invoice.updated_at.isoformat() if invoice.updated_at else None,
            'details': details
        }
    except Exception as e:
        raise Exception(f"Error converting invoice to dict: {str(e)}")


@owner_ai_invoice_bp.route('/create', methods=['POST'])
@token_required
def owner_create_ai_invoice():
    """
    Create draft invoice from natural language (Owner)
    
    Request body:
    {
        "text": "Lấy 5 bao xi măng cho anh Ba, ghi nợ"
    }
    
    Response:
    {
        "invoice": {...},
        "confidence": 0.85,
        "warnings": ["Không tìm thấy khách hàng: anh Ba"],
        "ai_result": {...}
    }
    
    ---
    tags:
      - Owner AI Invoices
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - text
          properties:
            text:
              type: string
              description: Natural language command in Vietnamese
              example: "Lấy 5 bao xi măng cho anh Ba, ghi nợ"
    responses:
      201:
        description: Draft invoice created successfully
      400:
        description: Bad request or validation error
      401:
        description: Unauthorized
    """
    try:
        data = request.get_json()
        user_input = data.get('text')
        
        if not user_input:
            return jsonify({'error': 'Missing text field'}), 400
        
        household_id = get_household_id_from_token()
        created_by = request.user.get('user_name')
        
        ai_service = get_ai_invoice_service()
        result = ai_service.create_draft_invoice_from_text(
            user_input=user_input,
            household_id=household_id,
            created_by=created_by
        )
        
        # Reload invoice with details
        from infrastructure.repositories.invoice_repository import InvoiceRepository
        from infrastructure.databases.session_utils import get_session
        session = get_session()
        invoice_repo = InvoiceRepository()
        invoice_repo.session = session
        invoice_with_details = invoice_repo.get_by_id(result['invoice'].id, household_id)
        
        # Load invoice details manually
        if invoice_with_details and hasattr(invoice_with_details, 'id'):
            from infrastructure.repositories.invoice_detail_repository import InvoiceDetailRepository
            detail_repo = InvoiceDetailRepository()
            detail_repo.session = session
            details = detail_repo.list_by_invoice_id(invoice_with_details.id, household_id)
            invoice_with_details.details = details
        
        # Send real-time notification to household members
        try:
            from app import get_socketio
            from services.notification_service import NotificationService
            
            socketio = get_socketio()
            if socketio:
                notification_service = NotificationService(socketio)
                notification_service.notify_ai_draft_created(
                    household_id=household_id,
                    invoice_id=invoice_with_details.id if invoice_with_details else result['invoice'].id,
                    invoice_data=invoice_to_dict(invoice_with_details if invoice_with_details else result['invoice']),
                    confidence=result['confidence'],
                    warnings=result['warnings']
                )
        except Exception as e:
            # Don't fail request if notification fails
            print(f"Failed to send notification: {str(e)}")
        
        return jsonify({
            'invoice': invoice_to_dict(invoice_with_details if invoice_with_details else result['invoice']),
            'confidence': result['confidence'],
            'warnings': result['warnings'],
            'ai_result': result['ai_result']
        }), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500


@employee_ai_invoice_bp.route('/create', methods=['POST'])
@token_required
def employee_create_ai_invoice():
    """
    Create draft invoice from natural language (Employee)
    
    Request body:
    {
        "text": "Bán 10 cây sắt phi 10 cho chị Lan, thanh toán tiền mặt"
    }
    
    Response:
    {
        "invoice": {...},
        "confidence": 0.9,
        "warnings": [],
        "ai_result": {...}
    }
    
    ---
    tags:
      - Employee AI Invoices
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - text
          properties:
            text:
              type: string
              description: Natural language command in Vietnamese
              example: "Bán 10 cây sắt phi 10 cho chị Lan"
    responses:
      201:
        description: Draft invoice created successfully
      400:
        description: Bad request or validation error
      401:
        description: Unauthorized
    """
    try:
        data = request.get_json()
        user_input = data.get('text')
        
        if not user_input:
            return jsonify({'error': 'Missing text field'}), 400
        
        household_id = get_household_id_from_token()
        created_by = request.user.get('user_name')
        
        ai_service = get_ai_invoice_service()
        result = ai_service.create_draft_invoice_from_text(
            user_input=user_input,
            household_id=household_id,
            created_by=created_by
        )
        
        # Reload invoice with details
        from infrastructure.repositories.invoice_repository import InvoiceRepository
        from infrastructure.databases.session_utils import get_session
        session = get_session()
        invoice_repo = InvoiceRepository()
        invoice_repo.session = session
        invoice_with_details = invoice_repo.get_by_id(result['invoice'].id, household_id)
        
        # Load invoice details manually
        if invoice_with_details and hasattr(invoice_with_details, 'id'):
            from infrastructure.repositories.invoice_detail_repository import InvoiceDetailRepository
            detail_repo = InvoiceDetailRepository()
            detail_repo.session = session
            details = detail_repo.list_by_invoice_id(invoice_with_details.id, household_id)
            invoice_with_details.details = details
        
        # Send real-time notification to household members
        try:
            from app import get_socketio
            from services.notification_service import NotificationService
            
            socketio = get_socketio()
            if socketio:
                notification_service = NotificationService(socketio)
                notification_service.notify_ai_draft_created(
                    household_id=household_id,
                    invoice_id=invoice_with_details.id if invoice_with_details else result['invoice'].id,
                    invoice_data=invoice_to_dict(invoice_with_details if invoice_with_details else result['invoice']),
                    confidence=result['confidence'],
                    warnings=result['warnings']
                )
        except Exception as e:
            # Don't fail request if notification fails
            print(f"Failed to send notification: {str(e)}")
        
        return jsonify({
            'invoice': invoice_to_dict(invoice_with_details if invoice_with_details else result['invoice']),
            'confidence': result['confidence'],
            'warnings': result['warnings'],
            'ai_result': result['ai_result']
        }), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500
