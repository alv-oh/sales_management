"""FastAPI bridge for the existing sales management modules.

This file intentionally reuses current module functions so the original CLI
behavior and data flow remain unchanged.
"""

from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

import algorithms
import customers
import products
import transactions


app = FastAPI(title="Sales Management API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ProductCreate(BaseModel):
    id: Optional[str] = None
    name: str = Field(min_length=1)
    price: float = Field(gt=0)
    stock_quantity: int = Field(ge=0)
    category: Optional[str] = None


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = Field(default=None, gt=0)
    stock_quantity: Optional[int] = Field(default=None, ge=0)
    category: Optional[str] = None


class CustomerCreate(BaseModel):
    id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    contact_info: str = Field(min_length=1)


class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    contact_info: Optional[str] = None


class CartItem(BaseModel):
    product_id: str = Field(min_length=1)
    quantity: int = Field(gt=0)


class SaleCreate(BaseModel):
    customer_id: str = Field(min_length=1)
    items: list[CartItem]
    discount_percent: Optional[float] = Field(default=None, ge=0, le=100)


def build_dashboard():
    sales = transactions.load_sales()
    all_products = products.load_products()
    all_customers = customers.load_customers()

    total_revenue = algorithms.calculate_total_revenue(sales)
    average_sale = algorithms.calculate_average_sale(sales)
    top_products = algorithms.top_selling_products(sales, top_n=5)
    low_stock_items = products.get_low_stock_products(5)

    return {
        "total_sales": len(sales),
        "total_revenue": total_revenue,
        "average_sale": average_sale,
        "total_products": len(all_products),
        "total_customers": len(all_customers),
        "low_stock_count": len(low_stock_items),
        "top_products": [
            {"product_id": pid, "name": name, "quantity_sold": qty}
            for pid, name, qty in top_products
        ],
    }


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/dashboard")
def dashboard():
    return build_dashboard()


@app.get("/api/products")
def list_products():
    return products.load_products()


@app.post("/api/products", status_code=201)
def create_product(payload: ProductCreate):
    existing = products.load_products()
    product_id = payload.id or products.generate_product_id(existing)

    ok = products.add_product(
        product_id,
        payload.name,
        payload.price,
        payload.stock_quantity,
        payload.category,
    )
    if not ok:
        raise HTTPException(status_code=400, detail="Product ID already exists.")

    created = products.find_product(product_id)
    return created


@app.put("/api/products/{product_id}")
def update_product(product_id: str, payload: ProductUpdate):
    ok = products.update_product(
        product_id,
        name=payload.name,
        price=payload.price,
        stock_quantity=payload.stock_quantity,
        category=payload.category,
    )
    if not ok:
        raise HTTPException(status_code=404, detail="Product not found.")

    return products.find_product(product_id)


@app.delete("/api/products/{product_id}")
def remove_product(product_id: str):
    ok = products.delete_product(product_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Product not found.")
    return {"message": "Deleted"}


@app.get("/api/customers")
def list_customers():
    return customers.load_customers()


@app.post("/api/customers", status_code=201)
def create_customer(payload: CustomerCreate):
    ok = customers.add_customer(payload.id, payload.name, payload.contact_info)
    if not ok:
        raise HTTPException(status_code=400, detail="Customer ID already exists.")
    return customers.find_customer(payload.id)


@app.put("/api/customers/{customer_id}")
def update_customer(customer_id: str, payload: CustomerUpdate):
    ok = customers.update_customer(
        customer_id,
        name=payload.name,
        contact_info=payload.contact_info,
    )
    if not ok:
        raise HTTPException(status_code=404, detail="Customer not found.")
    return customers.find_customer(customer_id)


@app.delete("/api/customers/{customer_id}")
def remove_customer(customer_id: str):
    ok = customers.delete_customer(customer_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Customer not found.")
    return {"message": "Deleted"}


@app.get("/api/sales")
def list_sales():
    return transactions.load_sales()


@app.post("/api/sales", status_code=201)
def create_sale(payload: SaleCreate):
    cart = []
    for item in payload.items:
        ok = transactions.add_to_cart(cart, item.product_id, item.quantity)
        if not ok:
            raise HTTPException(
                status_code=400,
                detail=f"Unable to add item {item.product_id} to cart.",
            )

    receipt = transactions.process_sale(
        payload.customer_id,
        cart,
        discount_percent=payload.discount_percent,
    )
    if receipt is None:
        raise HTTPException(status_code=400, detail="Sale could not be processed.")

    return receipt


@app.get("/api/reports/low-stock")
def report_low_stock(threshold: int = 5):
    return products.get_low_stock_products(threshold)


@app.get("/api/reports/top-products")
def report_top_products(top_n: int = 5):
    sales = transactions.load_sales()
    top = algorithms.top_selling_products(sales, top_n=top_n)
    return [
        {"product_id": pid, "name": name, "quantity_sold": qty}
        for pid, name, qty in top
    ]


@app.get("/api/reports/customer-activity")
def report_customer_activity():
    sales = transactions.load_sales()
    all_customers = customers.load_customers()
    counts = algorithms.sales_per_customer(sales)

    return [
        {
            "customer_id": c.get("id"),
            "name": c.get("name"),
            "transactions": counts.get(c.get("id"), 0),
        }
        for c in all_customers
    ]


@app.get("/api/reports/sorted-inventory")
def report_sorted_inventory(sort_by: str = "name", descending: bool = False):
    inventory = products.load_products()
    try:
        return algorithms.sort_products(inventory, by=sort_by, reverse=descending)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("web_api:app", host="127.0.0.1", port=8000, reload=True)
