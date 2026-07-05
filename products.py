# products.py

import json
import os

PRODUCTS_FILE = "products.json"

# ----------------------------
# Helper Functions
# ----------------------------

def load_products():
    """Load the list of products from the data file."""
    if not os.path.exists(PRODUCTS_FILE):
        return []

    try:
        with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_products(products):
    """Save the list of products back to the data file."""
    directory = os.path.dirname(PRODUCTS_FILE)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)

    with open(PRODUCTS_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=4)


def generate_product_id(products):
    return f"P{len(products) + 1:03d}"

# ----------------------------
# CREATE
# ----------------------------

def add_product(product_id, name, price, stock_quantity, category=None):
    """Add a new product. Returns True on success, False if ID already exists."""
    products = load_products()

    for product in products:
        if product["id"] == product_id:
            print(f"Error: Product with ID {product_id} already exists.")
            return False

    new_product = {
        "id": product_id,
        "name": name,
        "price": float(price),
        "stock_quantity": int(stock_quantity),
        "category": category,
    }
    products.append(new_product)
    save_products(products)
    print(f"Product '{name}' added successfully.")
    return True

# ----------------------------
# READ
# ----------------------------

def view_all_products():
    """Display all products in a readable table format."""
    products = load_products()

    if not products:
        print("No products found.")
        return

    print(f"{'ID':<6}{'Name':<20}{'Price':<10}{'Stock':<10}{'Category':<15}")
    print("-" * 61)
    for product in products:
        print(
            f"{product['id']:<6}"
            f"{product['name']:<20}"
            f"{product['price']:<10.2f}"
            f"{product['stock_quantity']:<10}"
            f"{(product['category'] or ''):<15}"
        )


def find_product(product_id):
    """Return a single product dict by ID, or None if not found."""
    products = load_products()
    for product in products:
        if product["id"] == product_id:
            return product
    return None

# ----------------------------
# UPDATE
# ----------------------------

def update_product(product_id, name=None, price=None, stock_quantity=None, category=None):
    """Update one or more fields of an existing product. Returns True/False."""
    products = load_products()

    for product in products:
        if product["id"] == product_id:
            if name is not None:
                product["name"] = name
            if price is not None:
                product["price"] = float(price)
            if stock_quantity is not None:
                product["stock_quantity"] = int(stock_quantity)
            if category is not None:
                product["category"] = category

            save_products(products)
            print(f"Product ID {product_id} updated successfully.")
            return True

    print(f"Error: Product with ID {product_id} not found.")
    return False

# ----------------------------
# DELETE
# ----------------------------

def delete_product(product_id):
    """Delete a product by ID. Returns True if deleted, False if not found."""
    products = load_products()
    updated_products = [p for p in products if p["id"] != product_id]

    if len(updated_products) == len(products):
        print(f"Error: Product with ID {product_id} not found.")
        return False

    save_products(updated_products)
    print(f"Product ID {product_id} deleted successfully.")
    return True

# ----------------------------
# Module helpers
# ----------------------------

def get_product_by_id(product_id):
    products = load_products()
    for p in products:
        if p["id"] == product_id:
            return p
    return None


def check_stock(product_id, quantity):
    product = get_product_by_id(product_id)
    if product:
        return product["stock_quantity"] >= quantity
    return False


def reduce_stock(product_id, quantity):
    products = load_products()
    for p in products:
        if p["id"] == product_id:
            if p["stock_quantity"] < quantity:
                return False
            p["stock_quantity"] -= quantity
            save_products(products)
            return True
    return False


def get_low_stock_products(threshold=5):
    products = load_products()
    return [p for p in products if p["stock_quantity"] <= threshold]
