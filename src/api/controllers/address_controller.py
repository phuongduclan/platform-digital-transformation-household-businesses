"""
Address Controller
API endpoints for address autocomplete and geolocation using Goong service
"""

from flask import Blueprint, request, jsonify
from external_services.goong_client import GoongClient
from api.utils.auth_utils import token_required
from config import Config

# Blueprint for address endpoints
owner_address_bp = Blueprint(
    'owner_addresses',
    __name__,
    url_prefix='/api/owner/addresses'
)

employee_address_bp = Blueprint(
    'employee_addresses',
    __name__,
    url_prefix='/api/employee/addresses'
)


def get_goong_client():
    """Initialize GoongClient with API key"""
    return GoongClient(api_key=Config.GOONG_API_KEY)


@owner_address_bp.route('/autocomplete', methods=['POST'])
@token_required
def owner_autocomplete_address():
    """
    Autocomplete address search
    
    Request body:
    {
        "query": "Hà Nội",
        "limit": 5
    }
    
    Response:
    [
        {
            "description": "Hà Nội, Việt Nam",
            "place_id": "...",
            "main_text": "Hà Nội",
            "secondary_text": "Việt Nam"
        }
    ]
    
    ---
    tags:
      - Owner Address
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - query
          properties:
            query:
              type: string
              description: Address search query
              example: "Hà Nội"
            limit:
              type: integer
              description: Maximum number of results (default 5)
              example: 5
    responses:
      200:
        description: Address suggestions returned
      400:
        description: Bad request
      401:
        description: Unauthorized
    """
    try:
        data = request.get_json()
        query = data.get('query')
        limit = data.get('limit', 5)
        
        if not query or len(query.strip()) < 2:
            return jsonify({'error': 'Query must be at least 2 characters'}), 400
        
        goong_client = get_goong_client()
        suggestions = goong_client.autocomplete(query, limit)
        
        return jsonify(suggestions), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to fetch suggestions: {str(e)}'}), 500


@owner_address_bp.route('/detail', methods=['POST'])
@token_required
def owner_get_address_detail():
    """
    Get detailed address information including coordinates
    
    Request body:
    {
        "place_id": "..."
    }
    
    Response:
    {
        "formatted_address": "...",
        "lat": 21.0285,
        "lng": 105.8542,
        "address_components": [...]
    }
    
    ---
    tags:
      - Owner Address
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - place_id
          properties:
            place_id:
              type: string
              description: Place ID from autocomplete result
    responses:
      200:
        description: Place details returned
      400:
        description: Bad request
      401:
        description: Unauthorized
    """
    try:
        data = request.get_json()
        place_id = data.get('place_id')
        
        if not place_id:
            return jsonify({'error': 'Missing place_id'}), 400
        
        goong_client = get_goong_client()
        detail = goong_client.get_place_detail(place_id)
        
        if not detail:
            return jsonify({'error': 'Place not found'}), 404
        
        return jsonify(detail), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to fetch place detail: {str(e)}'}), 500


@employee_address_bp.route('/autocomplete', methods=['POST'])
@token_required
def employee_autocomplete_address():
    """
    Autocomplete address search (Employee)
    
    Request body:
    {
        "query": "Hà Nội",
        "limit": 5
    }
    
    ---
    tags:
      - Employee Address
    security:
      - Bearer: []
    """
    try:
        data = request.get_json()
        query = data.get('query')
        limit = data.get('limit', 5)
        
        if not query or len(query.strip()) < 2:
            return jsonify({'error': 'Query must be at least 2 characters'}), 400
        
        goong_client = get_goong_client()
        suggestions = goong_client.autocomplete(query, limit)
        
        return jsonify(suggestions), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to fetch suggestions: {str(e)}'}), 500


@employee_address_bp.route('/detail', methods=['POST'])
@token_required
def employee_get_address_detail():
    """
    Get detailed address information including coordinates (Employee)
    
    Request body:
    {
        "place_id": "..."
    }
    
    ---
    tags:
      - Employee Address
    security:
      - Bearer: []
    """
    try:
        data = request.get_json()
        place_id = data.get('place_id')
        
        if not place_id:
            return jsonify({'error': 'Missing place_id'}), 400
        
        goong_client = get_goong_client()
        detail = goong_client.get_place_detail(place_id)
        
        if not detail:
            return jsonify({'error': 'Place not found'}), 404
        
        return jsonify(detail), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to fetch place detail: {str(e)}'}), 500
