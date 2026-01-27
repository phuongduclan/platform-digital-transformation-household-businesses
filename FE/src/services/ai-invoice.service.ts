import { api } from '@/lib/api';

export interface AIInvoiceRequest {
    text: string;
}

export interface AIInvoiceResponse {
    invoice: {
        id: number;
        household_id: number;
        customer_id: number | null;
        invoice_type: string;
        total_amount: number;
        status: string;
        description: string;
        created_at: string;
        updated_at: string;
    };
    confidence: number;
    warnings: string[];
    ai_result: {
        customer_name: string | null;
        invoice_type: string;
        items: Array<{
            product_name: string;
            quantity: number;
            unit_name: string | null;
        }>;
    };
}

export const aiInvoiceService = {
    /**
     * Create draft invoice from natural language text (Owner)
     */
    async createFromText(text: string): Promise<AIInvoiceResponse> {
        const response = await api.post<AIInvoiceResponse>(
            '/api/owner/ai-invoices/create',
            { text }
        );
        return response.data;
    }
};

export const employeeAIInvoiceService = {
    /**
     * Create draft invoice from natural language text (Employee)
     */
    async createFromText(text: string): Promise<AIInvoiceResponse> {
        const response = await api.post<AIInvoiceResponse>(
            '/api/employee/ai-invoices/create',
            { text }
        );
        return response.data;
    }
};
