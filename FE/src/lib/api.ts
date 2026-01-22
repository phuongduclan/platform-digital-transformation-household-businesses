import axios from 'axios';

export interface LoginResponse {
  token: string;
  user_id: number;
  role_id: number;
  household_id: number | null;
}

export interface SubscriptionPlanDto {
  id: number;
  name: string;
  price: number;
  billing_cycle?: string;
  description?: string;
}

export interface RegistrationPayload {
  plan_id: number;
  household: {
    name: string;
    tax_code?: string;
    phone?: string;
    address?: string;
    description?: string;
  };
  owner_account: {
    user_name: string;
    password: string;
    email?: string;
    description?: string;
  };
}

export interface RegistrationResponse {
  message: string;
  user_id?: number;
  household_id?: number;
}

export const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:6868',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to include the token
api.interceptors.request.use(
  (config) => {
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('auth_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);
