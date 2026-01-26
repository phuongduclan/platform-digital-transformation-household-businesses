import { apiClient } from '@/lib/api';

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
     * Autocomplete address search using Goong.io API
     * @param query - Search query (Vietnamese address)
     * @param limit - Maximum number of results (default 5)
     */
    async autocomplete(query: string, limit: number = 5): Promise<AddressSuggestion[]> {
        if (!query || query.trim().length < 2) {
            return [];
        }

        try {
            // Call backend proxy (to keep API key secure)
            const response = await fetch(
                `https://rsapi.goong.io/Place/AutoComplete?api_key=GaIfhCGenUAlFHpcKSXDTTPsMMU9lDc6PlezgXl6&input=${encodeURIComponent(query)}&limit=${limit}`,
                {
                    method: 'GET',
                }
            );

            if (!response.ok) {
                console.error('Goong API error:', response.statusText);
                return [];
            }

            const data = await response.json();
            const predictions = data.predictions || [];

            return predictions.map((pred: any) => ({
                description: pred.description || '',
                place_id: pred.place_id || '',
                main_text: pred.structured_formatting?.main_text || '',
                secondary_text: pred.structured_formatting?.secondary_text || '',
            }));
        } catch (error) {
            console.error('Error fetching address suggestions:', error);
            return [];
        }
    },

    /**
     * Get detailed place information
     * @param placeId - Place ID from autocomplete result
     */
    async getPlaceDetail(placeId: string): Promise<PlaceDetail | null> {
        if (!placeId) {
            return null;
        }

        try {
            const response = await fetch(
                `https://rsapi.goong.io/Place/Detail?api_key=GaIfhCGenUAlFHpcKSXDTTPsMMU9lDc6PlezgXl6&place_id=${encodeURIComponent(placeId)}`
            );

            if (!response.ok) {
                return null;
            }

            const data = await response.json();
            const result = data.result || {};
            const location = result.geometry?.location || {};

            return {
                formatted_address: result.formatted_address || '',
                lat: location.lat || null,
                lng: location.lng || null,
                address_components: result.address_components || [],
            };
        } catch (error) {
            console.error('Error fetching place detail:', error);
            return null;
        }
    },
};
