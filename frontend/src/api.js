const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

async function request(path, options = {}) {
  // Centralized fetch wrapper for error handling and JSON parsing.
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  if (!response.ok) {
    let message = "Request failed";
    try {
      const data = await response.json();
      message = data.detail || message;
    } catch (error) {
      message = response.statusText || message;
    }
    throw new Error(message);
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}

export const api = {
  // Dashboard
  getDashboard: () => request("/api/dashboard"),

  // Products
  getProducts: () => request("/api/products"),
  createProduct: (payload) =>
    request("/api/products", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  updateProduct: (id, payload) =>
    request(`/api/products/${id}`, {
      method: "PUT",
      body: JSON.stringify(payload),
    }),
  deleteProduct: (id) =>
    request(`/api/products/${id}`, {
      method: "DELETE",
    }),

  // Customers
  getCustomers: () => request("/api/customers"),
  createCustomer: (payload) =>
    request("/api/customers", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  updateCustomer: (id, payload) =>
    request(`/api/customers/${id}`, {
      method: "PUT",
      body: JSON.stringify(payload),
    }),
  deleteCustomer: (id) =>
    request(`/api/customers/${id}`, {
      method: "DELETE",
    }),

  // Sales
  getSales: () => request("/api/sales"),
  createSale: (payload) =>
    request("/api/sales", {
      method: "POST",
      body: JSON.stringify(payload),
    }),
};
