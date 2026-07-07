# products.py

"""Product catalog and inventory management operations."""

import json
import os

PRODUCTS_FILE = "products.json"


def _product_index(products_list):
    """Build a dictionary index keyed by product ID."""
    return {product.get("id"): product for product in products_list}


def _product_id_to_position(products_list):
    """Build a dictionary mapping product ID to list position."""
    return {product.get("id"): idx for idx, product in enumerate(products_list)}

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
    """Generate a simple sequential product ID based on current list size."""
    return f"P{len(products) + 1:03d}"

# ----------------------------
# CREATE
# ----------------------------

def add_product(product_id, name, price, stock_quantity, category=None):
    """Add a new product. Returns True on success, False if ID already exists."""
    products = load_products()
    product_index = _product_index(products)

    if product_id in product_index:
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
    return _product_index(products).get(product_id)

# ----------------------------
# UPDATE
# ----------------------------

def update_product(product_id, name=None, price=None, stock_quantity=None, category=None):
    """Update one or more fields of an existing product. Returns True/False."""
    products = load_products()
    id_to_position = _product_id_to_position(products)
    position = id_to_position.get(product_id)

    if position is not None:
        product = products[position]
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
    id_to_position = _product_id_to_position(products)
    position = id_to_position.get(product_id)

    if position is None:
        print(f"Error: Product with ID {product_id} not found.")
        return False

    products.pop(position)
    save_products(products)
    print(f"Product ID {product_id} deleted successfully.")
    return True

# ----------------------------
# Module helpers
# ----------------------------

def get_product_by_id(product_id):
    """Return product by ID or None when it does not exist."""
    products = load_products()
    return _product_index(products).get(product_id)


def check_stock(product_id, quantity):
    """Check whether a product has at least the requested quantity."""
    product = get_product_by_id(product_id)
    if product:
        return product["stock_quantity"] >= quantity
    return False


def reduce_stock(product_id, quantity):
    """Reduce stock for a product after a confirmed sale."""
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
    """Return products with stock at or below the configured threshold."""
    products = load_products()
    return [p for p in products if p["stock_quantity"] <= threshold]
