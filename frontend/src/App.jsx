import { useEffect, useMemo, useState } from "react";
import { api } from "./api";

const sections = ["Dashboard", "Products", "Customers", "Sales"];

function currency(value) {
  const num = Number(value || 0);
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "KES",
  }).format(num);
}

function EmptyState({ label }) {
  return <div className="empty">No {label} yet.</div>;
}

export default function App() {
  const [active, setActive] = useState("Dashboard");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [dashboard, setDashboard] = useState(null);
  const [products, setProducts] = useState([]);
  const [customers, setCustomers] = useState([]);
  const [sales, setSales] = useState([]);

  const [productForm, setProductForm] = useState({
    id: "",
    name: "",
    price: "",
    stock_quantity: "",
    category: "",
  });
  const [customerForm, setCustomerForm] = useState({
    id: "",
    name: "",
    contact_info: "",
  });

  const [saleForm, setSaleForm] = useState({
    customer_id: "",
    discount_percent: "",
    items: [{ product_id: "", quantity: 1 }],
  });

  async function refreshAll() {
    setLoading(true);
    setError("");
    try {
      const [dashboardData, productsData, customersData, salesData] = await Promise.all([
        api.getDashboard(),
        api.getProducts(),
        api.getCustomers(),
        api.getSales(),
      ]);

      setDashboard(dashboardData);
      setProducts(productsData);
      setCustomers(customersData);
      setSales(salesData);
    } catch (err) {
      setError(err.message || "Unable to fetch data.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    refreshAll();
  }, []);

  const productById = useMemo(() => {
    const map = new Map();
    products.forEach((p) => map.set(p.id, p));
    return map;
  }, [products]);

  async function onAddProduct(event) {
    event.preventDefault();
    setError("");
    try {
      await api.createProduct({
        id: productForm.id || null,
        name: productForm.name,
        price: Number(productForm.price),
        stock_quantity: Number(productForm.stock_quantity),
        category: productForm.category || null,
      });
      setProductForm({ id: "", name: "", price: "", stock_quantity: "", category: "" });
      await refreshAll();
    } catch (err) {
      setError(err.message);
    }
  }

  async function onDeleteProduct(id) {
    setError("");
    try {
      await api.deleteProduct(id);
      await refreshAll();
    } catch (err) {
      setError(err.message);
    }
  }

  async function onAddCustomer(event) {
    event.preventDefault();
    setError("");
    try {
      await api.createCustomer(customerForm);
      setCustomerForm({ id: "", name: "", contact_info: "" });
      await refreshAll();
    } catch (err) {
      setError(err.message);
    }
  }

  async function onDeleteCustomer(id) {
    setError("");
    try {
      await api.deleteCustomer(id);
      await refreshAll();
    } catch (err) {
      setError(err.message);
    }
  }

  function updateSaleItem(index, key, value) {
    setSaleForm((prev) => {
      const items = [...prev.items];
      items[index] = { ...items[index], [key]: value };
      return { ...prev, items };
    });
  }

  function addSaleItemLine() {
    setSaleForm((prev) => ({
      ...prev,
      items: [...prev.items, { product_id: "", quantity: 1 }],
    }));
  }

  function removeSaleItemLine(index) {
    setSaleForm((prev) => {
      const items = prev.items.filter((_, i) => i !== index);
      return {
        ...prev,
        items: items.length ? items : [{ product_id: "", quantity: 1 }],
      };
    });
  }

  async function onCreateSale(event) {
    event.preventDefault();
    setError("");

    const cleanedItems = saleForm.items
      .filter((item) => item.product_id)
      .map((item) => ({
        product_id: item.product_id,
        quantity: Number(item.quantity),
      }));

    try {
      await api.createSale({
        customer_id: saleForm.customer_id,
        discount_percent: saleForm.discount_percent === "" ? null : Number(saleForm.discount_percent),
        items: cleanedItems,
      });
      setSaleForm({
        customer_id: "",
        discount_percent: "",
        items: [{ product_id: "", quantity: 1 }],
      });
      await refreshAll();
      setActive("Dashboard");
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <h1>Sales Command Center</h1>
        <nav>
          {sections.map((name) => (
            <button
              key={name}
              className={name === active ? "nav-btn active" : "nav-btn"}
              onClick={() => setActive(name)}
            >
              {name}
            </button>
          ))}
        </nav>
      </aside>

      <main className="main-panel">
        <header className="hero">
          <h2>{active}</h2>
          <button className="refresh" onClick={refreshAll}>Refresh Data</button>
        </header>

        {error && <div className="error-banner">{error}</div>}
        {loading && <div className="loading">Loading data...</div>}

        {!loading && active === "Dashboard" && dashboard && (
          <section className="grid cards">
            <article className="card stat">
              <span>Revenue</span>
              <strong>{currency(dashboard.total_revenue)}</strong>
            </article>
            <article className="card stat">
              <span>Sales</span>
              <strong>{dashboard.total_sales}</strong>
            </article>
            <article className="card stat">
              <span>Average Sale</span>
              <strong>{currency(dashboard.average_sale)}</strong>
            </article>
            <article className="card stat">
              <span>Low Stock Products</span>
              <strong>{dashboard.low_stock_count}</strong>
            </article>

            <article className="card wide">
              <h3>Top Products</h3>
              {dashboard.top_products?.length ? (
                <div className="bars">
                  {dashboard.top_products.map((item) => (
                    <div key={item.product_id} className="bar-row">
                      <label>{item.name}</label>
                      <div className="bar-track">
                        <div
                          className="bar-fill"
                          style={{
                            width: `${Math.min(100, item.quantity_sold * 10)}%`,
                          }}
                        />
                      </div>
                      <span>{item.quantity_sold}</span>
                    </div>
                  ))}
                </div>
              ) : (
                <EmptyState label="sales" />
              )}
            </article>
          </section>
        )}

        {!loading && active === "Products" && (
          <section className="grid split">
            <article className="card">
              <h3>Add Product</h3>
              <form onSubmit={onAddProduct} className="form-grid">
                <input
                  placeholder="Product ID (optional)"
                  value={productForm.id}
                  onChange={(e) => setProductForm((p) => ({ ...p, id: e.target.value }))}
                />
                <input
                  required
                  placeholder="Name"
                  value={productForm.name}
                  onChange={(e) => setProductForm((p) => ({ ...p, name: e.target.value }))}
                />
                <input
                  required
                  type="number"
                  step="0.01"
                  min="0"
                  placeholder="Price"
                  value={productForm.price}
                  onChange={(e) => setProductForm((p) => ({ ...p, price: e.target.value }))}
                />
                <input
                  required
                  type="number"
                  min="0"
                  placeholder="Stock quantity"
                  value={productForm.stock_quantity}
                  onChange={(e) => setProductForm((p) => ({ ...p, stock_quantity: e.target.value }))}
                />
                <input
                  placeholder="Category (optional)"
                  value={productForm.category}
                  onChange={(e) => setProductForm((p) => ({ ...p, category: e.target.value }))}
                />
                <button type="submit">Create Product</button>
              </form>
            </article>

            <article className="card">
              <h3>Product Inventory</h3>
              {products.length ? (
                <table>
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Name</th>
                      <th>Price</th>
                      <th>Stock</th>
                      <th>Category</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {products.map((p) => (
                      <tr key={p.id}>
                        <td>{p.id}</td>
                        <td>{p.name}</td>
                        <td>{currency(p.price)}</td>
                        <td>{p.stock_quantity}</td>
                        <td>{p.category || "-"}</td>
                        <td>
                          <button className="danger" onClick={() => onDeleteProduct(p.id)}>
                            Delete
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              ) : (
                <EmptyState label="products" />
              )}
            </article>
          </section>
        )}

        {!loading && active === "Customers" && (
          <section className="grid split">
            <article className="card">
              <h3>Add Customer</h3>
              <form onSubmit={onAddCustomer} className="form-grid">
                <input
                  required
                  placeholder="Customer ID"
                  value={customerForm.id}
                  onChange={(e) => setCustomerForm((p) => ({ ...p, id: e.target.value }))}
                />
                <input
                  required
                  placeholder="Name"
                  value={customerForm.name}
                  onChange={(e) => setCustomerForm((p) => ({ ...p, name: e.target.value }))}
                />
                <input
                  required
                  placeholder="Contact info"
                  value={customerForm.contact_info}
                  onChange={(e) =>
                    setCustomerForm((p) => ({ ...p, contact_info: e.target.value }))
                  }
                />
                <button type="submit">Create Customer</button>
              </form>
            </article>

            <article className="card">
              <h3>Customer List</h3>
              {customers.length ? (
                <table>
                  <thead>
                    <tr>
                      <th>ID</th>
                      <th>Name</th>
                      <th>Contact</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {customers.map((c) => (
                      <tr key={c.id}>
                        <td>{c.id}</td>
                        <td>{c.name}</td>
                        <td>{c.contact_info}</td>
                        <td>
                          <button className="danger" onClick={() => onDeleteCustomer(c.id)}>
                            Delete
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              ) : (
                <EmptyState label="customers" />
              )}
            </article>
          </section>
        )}

        {!loading && active === "Sales" && (
          <section className="grid split">
            <article className="card">
              <h3>Process New Sale</h3>
              <form onSubmit={onCreateSale} className="form-grid">
                <select
                  required
                  value={saleForm.customer_id}
                  onChange={(e) => setSaleForm((prev) => ({ ...prev, customer_id: e.target.value }))}
                >
                  <option value="">Select customer</option>
                  {customers.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.id} - {c.name}
                    </option>
                  ))}
                </select>

                <input
                  type="number"
                  min="0"
                  max="100"
                  step="0.01"
                  placeholder="Discount % (optional)"
                  value={saleForm.discount_percent}
                  onChange={(e) =>
                    setSaleForm((prev) => ({ ...prev, discount_percent: e.target.value }))
                  }
                />

                <div className="line-items">
                  {saleForm.items.map((line, index) => {
                    const selected = productById.get(line.product_id);
                    return (
                      <div key={index} className="line-row">
                        <select
                          required
                          value={line.product_id}
                          onChange={(e) => updateSaleItem(index, "product_id", e.target.value)}
                        >
                          <option value="">Select product</option>
                          {products.map((p) => (
                            <option key={p.id} value={p.id}>
                              {p.id} - {p.name} ({p.stock_quantity} in stock)
                            </option>
                          ))}
                        </select>

                        <input
                          required
                          type="number"
                          min="1"
                          value={line.quantity}
                          onChange={(e) => updateSaleItem(index, "quantity", e.target.value)}
                        />

                        <button
                          type="button"
                          className="muted"
                          onClick={() => removeSaleItemLine(index)}
                        >
                          Remove
                        </button>

                        <span className="line-hint">
                          {selected ? `${selected.name} @ ${currency(selected.price)}` : ""}
                        </span>
                      </div>
                    );
                  })}
                </div>

                <button type="button" className="muted" onClick={addSaleItemLine}>
                  Add Another Item
                </button>
                <button type="submit">Process Sale</button>
              </form>
            </article>

            <article className="card">
              <h3>Recent Sales</h3>
              {sales.length ? (
                <table>
                  <thead>
                    <tr>
                      <th>Sale ID</th>
                      <th>Customer</th>
                      <th>Total</th>
                      <th>Date</th>
                    </tr>
                  </thead>
                  <tbody>
                    {sales
                      .slice()
                      .reverse()
                      .map((sale) => (
                        <tr key={sale.id}>
                          <td>{sale.id}</td>
                          <td>{sale.customer_name}</td>
                          <td>{currency(sale.total)}</td>
                          <td>{sale.timestamp}</td>
                        </tr>
                      ))}
                  </tbody>
                </table>
              ) : (
                <EmptyState label="sales" />
              )}
            </article>
          </section>
        )}
      </main>
    </div>
  );
}
