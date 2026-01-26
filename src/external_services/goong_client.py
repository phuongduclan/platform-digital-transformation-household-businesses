"""
Goong.io API Client
Vietnamese address autocomplete service
API Documentation: https://docs.goong.io
"""

import requests
from typing import List, Dict, Any, Optional
from config import Config


class GoongClient:
    """
    Client for Goong.io Place Autocomplete API
    Provides Vietnamese address search and geocoding
    """
    
    AUTOCOMPLETE_URL = "https://rsapi.goong.io/Place/AutoComplete"
    PLACE_DETAIL_URL = "https://rsapi.goong.io/Place/Detail"
    
    def __init__(self, api_key: str = None):
        """
        Initialize Goong client
        
        Args:
            api_key: Goong.io API key (defaults to Config.GOONG_API_KEY)
        """
        self.api_key = api_key or Config.GOONG_API_KEY
        if not self.api_key:
            raise ValueError("Goong.io API key is required. Set GOONG_API_KEY in .env")
    
    def autocomplete(
        self,
        query: str,
        limit: int = 5,
        location: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for address suggestions using autocomplete
        
        Args:
            query: Address search query (Vietnamese)
            limit: Maximum number of results (default 5)
            location: Optional lat,lng to bias results (e.g., "10.762622,106.660172")
        
        Returns:
            List of address suggestions:
            [
                {
                    'description': 'Full address',
                    'place_id': 'Unique place ID',
                    'main_text': 'Primary text',
                    'secondary_text': 'Secondary text (district, city)'
                }
            ]
        
        Example:
            >>> client = GoongClient()
            >>> results = client.autocomplete("48 Tô Hiến Thành")
            >>> results[0]['description']
            '48 Tô Hiến Thành, Phường 15, Quận 10, TP.HCM'
        """
        if not query or not query.strip():
            return []
        
        try:
            params = {
                'api_key': self.api_key,
                'input': query.strip(),
                'limit': min(limit, 10)  # Max 10
            }
            
            if location:
                params['location'] = location
            
            response = requests.get(
                self.AUTOCOMPLETE_URL,
                params=params,
                timeout=5  # 5 second timeout
            )
            
            response.raise_for_status()
            data = response.json()
            
            # Parse predictions
            predictions = data.get('predictions', [])
            results = []
            
            for pred in predictions:
                structured = pred.get('structured_formatting', {})
                results.append({
                    'description': pred.get('description', ''),
                    'place_id': pred.get('place_id', ''),
                    'main_text': structured.get('main_text', ''),
                    'secondary_text': structured.get('secondary_text', '')
                })
            
            return results
            
        except requests.exceptions.Timeout:
            print("Goong.io API timeout")
            return []
        except requests.exceptions.RequestException as e:
            print(f"Goong.io API error: {str(e)}")
            return []
        except Exception as e:
            print(f"Unexpected error in Goong autocomplete: {str(e)}")
            return []
    
    def get_place_detail(self, place_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a place (including lat/lng)
        
        Args:
            place_id: Place ID from autocomplete result
        
        Returns:
            {
                'formatted_address': 'Full formatted address',
                'lat': latitude,
                'lng': longitude,
                'address_components': [...]
            }
        """
        if not place_id:
            return None
        
        try:
            params = {
                'api_key': self.api_key,
                'place_id': place_id
            }
            
            response = requests.get(
                self.PLACE_DETAIL_URL,
                params=params,
                timeout=5
            )
            
            response.raise_for_status()
            data = response.json()
            
            result = data.get('result', {})
            geometry = result.get('geometry', {})
            location = geometry.get('location', {})
            
            return {
                'formatted_address': result.get('formatted_address', ''),
                'lat': location.get('lat'),
                'lng': location.get('lng'),
                'address_components': result.get('address_components', [])
            }
            
        except Exception as e:
            print(f"Error getting place detail: {str(e)}")
            return None
