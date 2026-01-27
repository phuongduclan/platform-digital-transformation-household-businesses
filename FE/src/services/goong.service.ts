import { api } from '@/lib/api';

export interface AddressSuggestion {
    description: string;
    place_id: string;
    main_text: string;
    secondary_text: string;
}

export interface PlaceDetail {
    formatted_address: string;
    lat: number | null;
    lng: number | null;
    address_components: any[];
}

export const goongService = {
    /**
     * Autocomplete address search using Goong.io API via backend proxy
     * @param query - Search query (Vietnamese address)
     * @param limit - Maximum number of results (default 5)
     */
    async autocomplete(query: string, limit: number = 5): Promise<AddressSuggestion[]> {
        if (!query || query.trim().length < 2) {
            return [];
        }

        try {
            // Call backend proxy - API key is kept secure on server
            const response = await api.post<AddressSuggestion[]>(
                '/api/owner/addresses/autocomplete',
                {
                    query: query.trim(),
                    limit
                }
            );

            return response.data || [];
        } catch (error) {
            console.error('Error fetching address suggestions:', error);
            return [];
        }
    },

    /**
     * Get detailed place information via backend proxy
     * @param placeId - Place ID from autocomplete result
     */
    async getPlaceDetail(placeId: string): Promise<PlaceDetail | null> {
        if (!placeId) {
            return null;
        }

        try {
            // Call backend proxy - API key is kept secure on server
            const response = await api.post<PlaceDetail>(
                '/api/owner/addresses/detail',
                {
                    place_id: placeId
                }
            );

            return response.data || null;
        } catch (error) {
            console.error('Error fetching place detail:', error);
            return null;
        }
    },
};
