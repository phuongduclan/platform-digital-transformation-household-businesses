import { api } from "@/lib/api";
import {
  OwnerCustomer,
  OwnerDebtRecord,
  OwnerInvoice,
  OwnerInvoiceDetail,
  OwnerPayment,
  OwnerPaymentMethod,
  OwnerProduct,
  OwnerUnit,
  OwnerSeller,
  OwnerInventory,
  OwnerWarehouse,
} from "@/services/owner.service";

// Employee dùng nhiều model giống Owner, nên tái sử dụng type từ owner.service

export interface EmployeeInvoice extends OwnerInvoice {}
export interface EmployeeInvoiceDetail extends OwnerInvoiceDetail {}
export interface EmployeePayment extends OwnerPayment {}
export interface EmployeeDebtRecord extends OwnerDebtRecord {}
export interface EmployeeInventory extends OwnerInventory {}

export const employeeService = {
  // Invoices (Employee)
  async listInvoices(params?: { status?: string }): Promise<EmployeeInvoice[]> {
    const res = await api.get("/api/employee/invoices", { params });
    return res.data || [];
  },

  async getInvoice(id: number): Promise<EmployeeInvoice> {
    const res = await api.get(`/api/employee/invoices/${id}`);
    return res.data;
  },

  async createInvoice(data: {
    seller_id?: number | null;
    customer_id?: number | null;
    invoice_type?: string;
    description?: string;
    details: Array<{
      product_id: number;
      unit_id: number;
      quantity: number;
      price: number;
      vat?: number;
      discount?: number;
      description?: string;
    }>;
  }): Promise<EmployeeInvoice> {
    const res = await api.post("/api/employee/invoices", data);
    return res.data;
  },

  async updateInvoice(
    id: number,
    data: {
      seller_id?: number | null;
      customer_id?: number | null;
      invoice_type?: string;
      description?: string;
    }
  ): Promise<EmployeeInvoice> {
    const res = await api.put(`/api/employee/invoices/${id}`, data);
    return res.data;
  },

  async deleteInvoice(id: number): Promise<void> {
    await api.delete(`/api/employee/invoices/${id}`);
  },

  async confirmInvoice(id: number): Promise<EmployeeInvoice> {
    const res = await api.put(`/api/employee/invoices/${id}/confirm`);
    return res.data;
  },

  async printInvoice(id: number): Promise<{
    invoice: EmployeeInvoice;
    household: {
      id: number;
      name: string | null;
      tax_code: string | null;
      address: string | null;
      phone: string | null;
      description: string | null;
    } | null;
    customer: {
      id: number;
      name: string | null;
      tax_code: string | null;
      address: string | null;
      phone: string | null;
    } | null;
    seller: {
      id: number;
      name: string | null;
      tax_code: string | null;
      address: string | null;
      phone: string | null;
    } | null;
    details: Array<{
      id: number;
      product_name: string;
      unit_name: string;
      quantity: number;
      price: string | null;
      discount: string | null;
      vat: number;
      line_total: string;
    }>;
  }> {
    const res = await api.get(`/api/employee/invoices/${id}/print`);
    return res.data;
  },

  // Invoice details (dùng endpoint chung)
  async listInvoiceDetails(invoiceId: number): Promise<EmployeeInvoiceDetail[]> {
    const res = await api.get(`/api/employee/invoices/${invoiceId}/details`);
    return res.data || [];
  },

  // Payments (Employee) - CHỈ có POST và GET detail, KHÔNG có list
  // Employee không có quyền list payments (F211 chỉ cho POST và GET detail)
  // Nếu cần list, phải dùng owner endpoint (F112) hoặc filter từ invoices

  async getPayment(id: number): Promise<EmployeePayment> {
    const res = await api.get(`/api/employee/payments/${id}`);
    return res.data;
  },

  async createPayment(data: {
    invoice_id: number;
    method_id: number;
    amount: number;
    description?: string;
  }): Promise<EmployeePayment> {
    const res = await api.post("/api/employee/payments", data);
    return res.data;
  },

  // Debt records (Employee - read-only)
  async listDebtRecords(params?: {
    customer_id?: number;
  }): Promise<EmployeeDebtRecord[]> {
    const res = await api.get("/api/employee/debt-records", { params });
    return res.data || [];
  },

  async getDebtRecord(id: number): Promise<EmployeeDebtRecord> {
    const res = await api.get(`/api/employee/debt-records/${id}`);
    return res.data;
  },

  async getCustomerDebtRecords(customerId: number): Promise<{
    customer_id: number;
    current_balance: string | null;
    debt_records: EmployeeDebtRecord[];
  }> {
    const res = await api.get(
      `/api/employee/debt-records/customer/${customerId}`
    );
    return res.data;
  },

  // Customers (Employee - read-only, dùng endpoint riêng, không dùng owner F109)
  async listCustomers(params?: { status?: string }): Promise<OwnerCustomer[]> {
    const res = await api.get("/api/employee/customers", { params });
    return res.data || [];
  },

  async listPaymentMethods(): Promise<OwnerPaymentMethod[]> {
    const res = await api.get("/api/owner/payment-methods");
    return res.data || [];
  },

  async listProducts(params?: { status?: string }): Promise<OwnerProduct[]> {
    const res = await api.get("/api/employee/products", { params });
    return res.data || [];
  },

  async listUnits(params?: { status?: string }): Promise<OwnerUnit[]> {
    const res = await api.get("/api/employee/units", { params });
    return res.data || [];
  },

  // Inventory (Employee - read-only, dùng endpoint riêng)
  async listInventory(params?: {
    warehouse_id?: number;
    product_id?: number;
    unit_id?: number;
  }): Promise<EmployeeInventory[]> {
    const res = await api.get("/api/employee/inventory", { params });
    return res.data || [];
  },

  async getInventoryDetail(
    product_id: number,
    warehouse_id: number,
    params?: { unit_id?: number }
  ): Promise<EmployeeInventory> {
    const res = await api.get(
      `/api/employee/inventory/${product_id}/${warehouse_id}`,
      { params }
    );
    return res.data;
  },

  // Warehouses (Employee - read-only, dùng endpoint riêng, không dùng F107 của Owner)
  async listWarehouses(): Promise<OwnerWarehouse[]> {
    const res = await api.get("/api/employee/warehouses");
    return res.data || [];
  },
};

