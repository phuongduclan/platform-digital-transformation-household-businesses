import { api } from "@/lib/api";

export interface OwnerDashboardStats {
  today_revenue: number;
  month_revenue: number;
  total_invoices: number;
  total_outstanding_debt: number;
}

export interface OwnerRevenuePoint {
  date: string;
  total_revenue: number;
}

export interface OwnerDebtPoint {
  customer_id: number;
  balance: number;
}



export interface OwnerEmployee {
  id: number;
  household_id: number | null;
  role_id: number;
  user_name: string;
  email: string | null;
  description: string | null;
  status: string;
  created_by: string | null;
  updated_by: string | null;
  created_at: string;
  updated_at: string;
}

export interface OwnerHousehold {
  id: number;
  tax_code?: string | null;
  name?: string | null;
  phone?: string | null;
  address?: string | null;
  description?: string | null;
  status: string;
  created_by?: string | null;
  updated_by?: string | null;
  created_at: string;
  updated_at: string;
}

export interface OwnerSubscription {
  id: number;
  plan_id: number;
  household_id: number;
  start_date: string;
  end_date: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface OwnerSubscriptionPlan {
  id: number;
  name: string;
  price: number;
  billing_cycle: string;
  description?: string | null;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface OwnerCategory {
  id: number;
  household_id: number;
  name: string;
  description?: string | null;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface OwnerUnit {
  id: number;
  household_id: number;
  name: string;
  description?: string | null;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface OwnerProduct {
  id: number;
  household_id: number;
  category_id: number;
  name: string;
  image_url?: string | null;
  description?: string | null;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface OwnerWarehouse {
  id: number;
  household_id: number;
  name: string;
  address: string;
  description?: string | null;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface OwnerInventory {
  id: number;
  product_id: number;
  unit_id: number;
  warehouse_id: number;
  quantity: number;
  created_at: string;
  updated_at: string;
}

export interface OwnerInvoice {
  id: number;
  household_id: number;
  seller_id: number | null;
  customer_id: number | null;
  invoice_type: string;
  discount_total: string | null;
  vat_total: string | null;
  total_amount: string | null;
  description: string | null;
  status: string;
  created_by: string | null;
  updated_by: string | null;
  invoice_number?: string;
  customer_name?: string | null;
  created_at: string;
  updated_at: string;
}

export interface OwnerInvoiceDetail {
  id: number;
  invoice_id: number;
  product_id: number;
  unit_id: number;
  vat: number;
  discount: number;
  price: string | null;
  description: string | null;
  quantity: number;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface OwnerImportReceipt {
  id: number;
  warehouse_id: number;
  invoice_id: number;
  import_date: string | null;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface OwnerExportReceipt {
  id: number;
  warehouse_id: number;
  invoice_id: number;
  export_date: string | null;
  reason: string | null;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface OwnerCustomer {
  id: number;
  household_id: number;
  tax_code?: string | null;
  name: string;
  phone?: string | null;
  address?: string | null;
  description?: string | null;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface OwnerSeller {
  id: number;
  household_id: number;
  tax_code?: string | null;
  name: string;
  phone?: string | null;
  address?: string | null;
  description?: string | null;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface OwnerPayment {
  id: number;
  invoice_id: number;
  method_id: number;
  amount: string | null;
  description: string | null;
  status: string;
  created_by: string | null;
  updated_by: string | null;
  created_at: string;
  updated_at: string;
}

export interface OwnerPaymentMethod {
  id: number;
  name: string;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface OwnerDebtRecord {
  id: number;
  customer_id: number;
  invoice_id: number | null;
  payment_id: number | null;
  debit_amount: string | null;
  credit_amount: string | null;
  balance: string | null;
  description: string | null;
  record_at: string | null;
}

export interface OwnerAccountingLedger {
  id: number;
  invoice_id: number | null;
  transaction_date: string | null;
  description: string | null;
  debit_amount: string | null;
  credit_amount: string | null;
  balance: string | null;
  document_number: string | null;
  movement_type: string | null;
  status: string | null;
  created_at: string | null;
  updated_at: string | null;
}

export const ownerService = {
  async getDailyRevenue(date: string): Promise<OwnerRevenuePoint> {
    const res = await api.get("/api/owner/reports/daily-revenue", {
      params: { date },
    });
    return {
      date: res.data.date,
      total_revenue: Number(res.data.total_revenue ?? 0),
    };
  },

  async getMonthlyRevenue(month: number, year: number): Promise<number> {
    const res = await api.get("/api/owner/reports/monthly-revenue", {
      params: { month, year },
    });
    return Number(res.data.total_revenue ?? 0);
  },

  async getOutstandingDebt(): Promise<OwnerDebtPoint[]> {
    const res = await api.get("/api/owner/reports/outstanding-debt");
    const raw = res.data?.outstanding_debts || res.data;
    const items: any[] = Array.isArray(raw) ? raw : [];
    return items.map((x) => ({
      customer_id: x.customer_id,
      balance: Number(x.balance ?? 0),
    }));
  },

  // Accounting ledgers (Owner)
  async listAccountingLedgers(params?: {
    from_date?: string;
    to_date?: string;
    movement_type?: string;
  }): Promise<OwnerAccountingLedger[]> {
    const res = await api.get("/api/owner/accounting-ledgers", { params });
    return res.data || [];
  },

  async getAccountingLedger(id: number): Promise<OwnerAccountingLedger> {
    const res = await api.get(`/api/owner/accounting-ledgers/${id}`);
    return res.data;
  },

  async listInvoices(params?: { status?: string }): Promise<OwnerInvoice[]> {
    const res = await api.get("/api/owner/invoices", { params });
    return res.data || [];
  },

  // Employees (Owner)
  async listEmployees(): Promise<OwnerEmployee[]> {
    const res = await api.get("/api/owner/employees/");
    return res.data || [];
  },

  async getEmployee(id: number): Promise<OwnerEmployee> {
    const res = await api.get(`/api/owner/employees/${id}`);
    return res.data;
  },

  async createEmployee(data: {
    user_name: string;
    password: string;
    email?: string;
    description?: string;
    status: string;
  }): Promise<OwnerEmployee> {
    const payload = {
      role_id: 3, // Employee
      user_name: data.user_name,
      password: data.password,
      email: data.email,
      description: data.description,
      status: data.status,
    };
    const res = await api.post("/api/owner/employees/", payload);
    return res.data;
  },

  async updateEmployee(
    id: number,
    data: {
      user_name?: string;
      password?: string;
      email?: string;
      description?: string;
      status?: string;
    }
  ): Promise<OwnerEmployee> {
    const res = await api.put(`/api/owner/employees/${id}`, data);
    return res.data;
  },

  async deleteEmployee(id: number): Promise<void> {
    await api.delete(`/api/owner/employees/${id}`);
  },

  // Household profile (Owner)
  async getHousehold(): Promise<OwnerHousehold> {
    const res = await api.get("/api/owner/household");
    return res.data;
  },

  async updateHousehold(data: {
    tax_code?: string | null;
    name?: string | null;
    phone?: string | null;
    address?: string | null;
    description?: string | null;
    status?: string | null;
    updated_by?: string | null;
  }): Promise<OwnerHousehold> {
    const res = await api.put("/api/owner/household", data);
    return res.data;
  },

  // Subscription (Owner)
  async getSubscription(): Promise<OwnerSubscription | null> {
    try {
      const res = await api.get("/api/owner/subscription");
      return res.data;
    } catch (error: any) {
      // Nếu household chưa có subscription, BE có thể trả 404 hoặc message khác -> coi như null
      if (error?.response?.status === 404) {
        return null;
      }
      throw error;
    }
  },

  async listActiveSubscriptionPlans(): Promise<OwnerSubscriptionPlan[]> {
    const res = await api.get("/api/owner/subscription-plans");
    return res.data || [];
  },

  async upgradeSubscription(data: {
    plan_id: number;
    start_date?: string;
    end_date?: string;
  }): Promise<OwnerSubscription> {
    const res = await api.put("/api/owner/subscription", data);
    return res.data;
  },

  // Catalogs: products, categories, units
  async listCategories(): Promise<OwnerCategory[]> {
    const res = await api.get("/api/owner/categories");
    return res.data || [];
  },

  async createCategory(data: {
    name: string;
    description?: string;
    status?: string;
  }): Promise<OwnerCategory> {
    const res = await api.post("/api/owner/categories", data);
    return res.data;
  },

  async updateCategory(
    id: number,
    data: {
      name?: string;
      description?: string;
      status?: string;
    }
  ): Promise<OwnerCategory> {
    const res = await api.put(`/api/owner/categories/${id}`, data);
    return res.data;
  },

  async deleteCategory(id: number): Promise<void> {
    await api.delete(`/api/owner/categories/${id}`);
  },

  async listUnits(): Promise<OwnerUnit[]> {
    const res = await api.get("/api/owner/units");
    return res.data || [];
  },

  async createUnit(data: {
    name: string;
    description?: string;
    status?: string;
  }): Promise<OwnerUnit> {
    const res = await api.post("/api/owner/units", data);
    return res.data;
  },

  async updateUnit(
    id: number,
    data: {
      name?: string;
      description?: string;
      status?: string;
    }
  ): Promise<OwnerUnit> {
    const res = await api.put(`/api/owner/units/${id}`, data);
    return res.data;
  },

  async deleteUnit(id: number): Promise<void> {
    await api.delete(`/api/owner/units/${id}`);
  },

  async listProducts(): Promise<OwnerProduct[]> {
    const res = await api.get("/api/owner/products");
    return res.data || [];
  },

  async createProduct(data: {
    category_id: number;
    name: string;
    image_url?: string;
    description?: string;
    status?: string;
  }): Promise<OwnerProduct> {
    const res = await api.post("/api/owner/products", data);
    return res.data;
  },

  async updateProduct(
    id: number,
    data: {
      category_id?: number;
      name?: string;
      image_url?: string;
      description?: string;
      status?: string;
    }
  ): Promise<OwnerProduct> {
    const res = await api.put(`/api/owner/products/${id}`, data);
    return res.data;
  },

  async deleteProduct(id: number): Promise<void> {
    await api.delete(`/api/owner/products/${id}`);
  },

  // Warehouses
  async listWarehouses(): Promise<OwnerWarehouse[]> {
    const res = await api.get("/api/owner/warehouses");
    return res.data || [];
  },

  async createWarehouse(data: {
    name: string;
    address: string;
    description?: string;
    status?: string;
  }): Promise<OwnerWarehouse> {
    const res = await api.post("/api/owner/warehouses", data);
    return res.data;
  },

  async updateWarehouse(
    id: number,
    data: {
      name?: string;
      address?: string;
      description?: string;
      status?: string;
    }
  ): Promise<OwnerWarehouse> {
    const res = await api.put(`/api/owner/warehouses/${id}`, data);
    return res.data;
  },

  async deleteWarehouse(id: number): Promise<void> {
    await api.delete(`/api/owner/warehouses/${id}`);
  },

  // Inventory
  async listInventory(params?: {
    warehouse_id?: number;
    product_id?: number;
    unit_id?: number;
  }): Promise<OwnerInventory[]> {
    const res = await api.get("/api/owner/inventory", { params });
    return res.data || [];
  },

  async getInventoryDetail(
    product_id: number,
    warehouse_id: number,
    params?: { unit_id?: number }
  ): Promise<OwnerInventory> {
    const res = await api.get(
      `/api/owner/inventory/${product_id}/${warehouse_id}`,
      { params }
    );
    return res.data;
  },

  // Invoices (Owner)
  async listInvoicesOwner(params?: { status?: string }): Promise<OwnerInvoice[]> {
    const res = await api.get("/api/owner/invoices", { params });
    return res.data || [];
  },

  async getInvoice(id: number): Promise<OwnerInvoice> {
    const res = await api.get(`/api/owner/invoices/${id}`);
    return res.data;
  },

  async createInvoice(data: {
    seller_id?: number | null;
    customer_id?: number | null;
    invoice_type?: string;
    description?: string;
    status?: string;
    details: Array<{
      product_id: number;
      unit_id: number;
      quantity: number;
      price: number;
      vat?: number;
      discount?: number;
      description?: string;
    }>;
  }): Promise<OwnerInvoice> {
    const res = await api.post("/api/owner/invoices", data);
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
  ): Promise<OwnerInvoice> {
    const res = await api.put(`/api/owner/invoices/${id}`, data);
    return res.data;
  },

  async deleteInvoice(id: number): Promise<void> {
    await api.delete(`/api/owner/invoices/${id}`);
  },

  async confirmInvoice(id: number): Promise<OwnerInvoice> {
    const res = await api.put(`/api/owner/invoices/${id}/confirm`);
    return res.data;
  },

  async printInvoice(id: number): Promise<{
    invoice: OwnerInvoice;
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
    const res = await api.get(`/api/owner/invoices/${id}/print`);
    return res.data;
  },

  // Invoice details (Owner)
  async listInvoiceDetails(invoiceId: number): Promise<OwnerInvoiceDetail[]> {
    const res = await api.get(`/api/invoices/${invoiceId}/details`);
    return res.data || [];
  },

  async createInvoiceDetail(
    invoiceId: number,
    data: {
      product_id: number;
      unit_id: number;
      quantity: number;
      price: number;
      vat?: number;
      discount?: number;
      description?: string;
      status?: string;
    }
  ): Promise<OwnerInvoiceDetail> {
    const res = await api.post(`/api/invoices/${invoiceId}/details`, data);
    return res.data;
  },

  async updateInvoiceDetail(
    invoiceId: number,
    detailId: number,
    data: {
      product_id?: number;
      unit_id?: number;
      quantity?: number;
      price?: number;
      vat?: number;
      discount?: number;
      description?: string;
      status?: string;
    }
  ): Promise<OwnerInvoiceDetail> {
    const res = await api.put(
      `/api/invoices/${invoiceId}/details/${detailId}`,
      data
    );
    return res.data;
  },

  async deleteInvoiceDetail(
    invoiceId: number,
    detailId: number
  ): Promise<void> {
    await api.delete(`/api/invoices/${invoiceId}/details/${detailId}`);
  },

  // Import receipts (Owner - R/U)
  async listImportReceipts(): Promise<OwnerImportReceipt[]> {
    const res = await api.get("/api/owner/import-receipts");
    return res.data || [];
  },

  async getImportReceipt(id: number): Promise<OwnerImportReceipt> {
    const res = await api.get(`/api/owner/import-receipts/${id}`);
    return res.data;
  },

  async updateImportReceipt(
    id: number,
    data: { warehouse_id?: number; import_date?: string }
  ): Promise<OwnerImportReceipt> {
    const res = await api.put(`/api/owner/import-receipts/${id}`, data);
    return res.data;
  },

  async listImportReceiptDetails(importId: number): Promise<{
    id: number;
    import_id: number;
    product_id: number;
    unit_id: number;
    quantity: number;
  }[]> {
    const res = await api.get(`/api/owner/import-receipts/${importId}/details`);
    return res.data || [];
  },

  // Export receipts (Owner - R/U)
  async listExportReceipts(): Promise<OwnerExportReceipt[]> {
    const res = await api.get("/api/owner/export-receipts");
    return res.data || [];
  },

  async getExportReceipt(id: number): Promise<OwnerExportReceipt> {
    const res = await api.get(`/api/owner/export-receipts/${id}`);
    return res.data;
  },

  async updateExportReceipt(
    id: number,
    data: { warehouse_id?: number; export_date?: string; reason?: string }
  ): Promise<OwnerExportReceipt> {
    const res = await api.put(`/api/owner/export-receipts/${id}`, data);
    return res.data;
  },

  async listExportReceiptDetails(exportId: number): Promise<{
    id: number;
    export_id: number;
    product_id: number;
    unit_id: number;
    quantity: number;
  }[]> {
    const res = await api.get(`/api/owner/export-receipts/${exportId}/details`);
    return res.data || [];
  },

  // Customers & Sellers (for selection)
  async listCustomers(params?: { status?: string }): Promise<OwnerCustomer[]> {
    const res = await api.get("/api/owner/customers", { params });
    return res.data || [];
  },

  async getCustomer(id: number): Promise<OwnerCustomer> {
    const res = await api.get(`/api/owner/customers/${id}`);
    return res.data;
  },

  async createCustomer(data: {
    tax_code?: string;
    name: string;
    phone?: string;
    address?: string;
    description?: string;
    status?: string;
  }): Promise<OwnerCustomer> {
    const res = await api.post("/api/owner/customers", data);
    return res.data;
  },

  async updateCustomer(
    id: number,
    data: {
      tax_code?: string;
      name?: string;
      phone?: string;
      address?: string;
      description?: string;
      status?: string;
    }
  ): Promise<OwnerCustomer> {
    const res = await api.put(`/api/owner/customers/${id}`, data);
    return res.data;
  },

  async deleteCustomer(id: number): Promise<void> {
    await api.delete(`/api/owner/customers/${id}`);
  },

  async listSellers(params?: { status?: string }): Promise<OwnerSeller[]> {
    const res = await api.get("/api/owner/sellers", { params });
    return res.data || [];
  },

  async getSeller(id: number): Promise<OwnerSeller> {
    const res = await api.get(`/api/owner/sellers/${id}`);
    return res.data;
  },

  async createSeller(data: {
    tax_code?: string;
    name: string;
    phone?: string;
    address?: string;
    description?: string;
    status?: string;
  }): Promise<OwnerSeller> {
    const res = await api.post("/api/owner/sellers", data);
    return res.data;
  },

  async updateSeller(
    id: number,
    data: {
      tax_code?: string;
      name?: string;
      phone?: string;
      address?: string;
      description?: string;
      status?: string;
    }
  ): Promise<OwnerSeller> {
    const res = await api.put(`/api/owner/sellers/${id}`, data);
    return res.data;
  },

  async deleteSeller(id: number): Promise<void> {
    await api.delete(`/api/owner/sellers/${id}`);
  },

  // Payments (Owner)
  async listPayments(params?: {
    invoice_id?: number;
    customer_id?: number;
  }): Promise<OwnerPayment[]> {
    const res = await api.get("/api/owner/payments", { params });
    return res.data || [];
  },

  async getPayment(id: number): Promise<OwnerPayment> {
    const res = await api.get(`/api/owner/payments/${id}`);
    return res.data;
  },

  async createPayment(data: {
    invoice_id: number;
    method_id: number;
    amount: number;
    description?: string;
  }): Promise<OwnerPayment> {
    const res = await api.post("/api/owner/payments", data);
    return res.data;
  },

  async updatePayment(
    id: number,
    data: {
      method_id?: number;
      amount?: number;
      description?: string;
    }
  ): Promise<OwnerPayment> {
    const res = await api.put(`/api/owner/payments/${id}`, data);
    return res.data;
  },

  async deletePayment(id: number): Promise<void> {
    await api.delete(`/api/owner/payments/${id}`);
  },

  async listOwnerPaymentMethods(): Promise<OwnerPaymentMethod[]> {
    const res = await api.get("/api/owner/payment-methods");
    return res.data || [];
  },

  // Debt records (Owner - read-only)
  async listDebtRecords(params?: {
    customer_id?: number;
  }): Promise<OwnerDebtRecord[]> {
    const res = await api.get("/api/owner/debt-records", { params });
    return res.data || [];
  },

  async getDebtRecord(id: number): Promise<OwnerDebtRecord> {
    const res = await api.get(`/api/owner/debt-records/${id}`);
    return res.data;
  },

  async getCustomerDebtRecords(customerId: number): Promise<{
    customer_id: number;
    current_balance: string | null;
    debt_records: OwnerDebtRecord[];
  }> {
    const res = await api.get(
      `/api/owner/debt-records/customer/${customerId}`
    );
    return res.data;
  },
};

