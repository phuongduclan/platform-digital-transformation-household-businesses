import { api } from "@/lib/api";

export interface User {
  id: number;
  household_id: number | null;
  role_id: number;
  user_name: string;
  email: string | null;
  status: string;
  description: string | null;
  created_by: string | null;
  updated_by: string | null;
  created_at: string;
  updated_at: string;
}

export interface UserListParams {
  role_id?: number;
  status?: string;
  household_id?: number;
  search?: string;
}

export const adminService = {
  // Users
  async listUsers(params?: UserListParams): Promise<User[]> {
    // Clean params - remove undefined values
    const cleanParams = params ? Object.fromEntries(
      Object.entries(params).filter(([_, v]) => v !== undefined && v !== null && v !== "")
    ) : undefined;
    
    const response = await api.get("/api/admin/users", { 
      params: cleanParams 
    });
    return response.data;
  },

  async getUser(id: number): Promise<User> {
    const response = await api.get(`/api/admin/users/${id}`);
    return response.data;
  },

  async createUser(data: any): Promise<User> {
    const response = await api.post("/api/admin/users", data);
    return response.data;
  },

  async updateUser(id: number, data: any): Promise<User> {
    const response = await api.put(`/api/admin/users/${id}`, data);
    return response.data;
  },

  async deleteUser(id: number): Promise<void> {
    await api.delete(`/api/admin/users/${id}`);
  },

  // Subscription Plans
  async listSubscriptionPlans(): Promise<any[]> {
    const response = await api.get("/api/admin/subscription-plans");
    return response.data;
  },

  async getSubscriptionPlan(id: number): Promise<any> {
    const response = await api.get(`/api/admin/subscription-plans/${id}`);
    return response.data;
  },

  async createSubscriptionPlan(data: any): Promise<any> {
    const response = await api.post("/api/admin/subscription-plans", data);
    return response.data;
  },

  async updateSubscriptionPlan(id: number, data: any): Promise<any> {
    const response = await api.put(`/api/admin/subscription-plans/${id}`, data);
    return response.data;
  },

  async deleteSubscriptionPlan(id: number): Promise<void> {
    await api.delete(`/api/admin/subscription-plans/${id}`);
  },

  // Subscriptions
  async listSubscriptions(params?: any): Promise<any[]> {
    const response = await api.get("/api/admin/subscriptions", { params });
    return response.data;
  },


  async updateSubscription(id: number, data: any): Promise<any> {
    const response = await api.put(`/api/admin/subscriptions/${id}`, data);
    return response.data;
  },

  // Households - REMOVED: Admin không có quyền quản lý Household (chỉ Owner có F102)
  // Các methods này đã bị xóa vì BE không có API Admin cho households
  // Nếu cần hiển thị household name, có thể lấy từ subscription data hoặc chỉ hiển thị household_id

  // Payment Methods
  async listPaymentMethods(params?: any): Promise<any[]> {
    const response = await api.get("/api/admin/payment-methods", { params });
    return response.data;
  },

  async getPaymentMethod(id: number): Promise<any> {
    const response = await api.get(`/api/admin/payment-methods/${id}`);
    return response.data;
  },

  async createPaymentMethod(data: any): Promise<any> {
    const response = await api.post("/api/admin/payment-methods", data);
    return response.data;
  },

  async updatePaymentMethod(id: number, data: any): Promise<any> {
    const response = await api.put(`/api/admin/payment-methods/${id}`, data);
    return response.data;
  },

  async deletePaymentMethod(id: number): Promise<void> {
    await api.delete(`/api/admin/payment-methods/${id}`);
  },

  // Dashboard Stats
  async getDashboardStats(): Promise<any> {
    const response = await api.get("/api/admin/dashboard/stats");
    return response.data;
  },

  // Analytics
  async getAnalytics(): Promise<any> {
    const response = await api.get("/api/admin/dashboard/analytics");
    return response.data;
  },
};
