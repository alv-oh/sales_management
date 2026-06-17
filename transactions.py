"""
 Product Management Module
-------------------------------------
Handles CRUD (Create, Read, Update, Delete) operations for products.

Each product is stored as a dictionary with the keys:
    id, name, price, stock_quantity

NOTE ON FILE INTEGRATION (Person 1):
This module assumes Person 1 is responsible for the actual reading/writing
of the shared data file (e.g. products.json or products.csv). Below,
`load_products()` and `save_products()` are placeholder wrappers around
simple JSON file I/O. If Person 1 already has functions for this
(e.g. in a file_handler.py module), simply replace the bodies of
`load_products()` and `save_products()` with calls to their functions,
for example:

    from file_handler import load_data, save_data
    def load_products():
        return load_data()
    def save_products(products):
        save_data(products)

This keeps Person 2's CRUD logic completely separate from how the
file is actually stored, so the two modules can be merged easily.
"""

import json
import os

DATA_FILE = "products.json"


# ---------------------------------------------------------------------
# File handling helpers (replace with Person 1's functions if available)
# ---------------------------------------------------------------------
def load_products():
    """Load the list of products from the data file."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_products(products):
    """Save the list of products back to the data file."""
    with open(DATA_FILE, "w") as f:
        json.dump(products, f, indent=4)


# ---------------------------------------------------------------------
# CREATE
# ---------------------------------------------------------------------
def add_product(product_id, name, price, stock_quantity):
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
    }
    products.append(new_product)
    save_products(products)
    print(f"Product '{name}' added successfully.")
    return True


# ---------------------------------------------------------------------
# READ
# ---------------------------------------------------------------------
def view_all_products():
    """Display all products in a readable table format."""
    products = load_products()

    if not products:
        print("No products found.")
        return

    print(f"{'ID':<6}{'Name':<20}{'Price':<10}{'Stock':<10}")
    print("-" * 46)
    for product in products:
        print(
            f"{product['id']:<6}{product['name']:<20}"
            f"{product['price']:<10.2f}{product['stock_quantity']:<10}"
        )


def find_product(product_id):
    """Return a single product dict by ID, or None if not found."""
    products = load_products()
    for product in products:
        if product["id"] == product_id:
            return product
    return None


# ---------------------------------------------------------------------
# UPDATE
# ---------------------------------------------------------------------
def update_product(product_id, name=None, price=None, stock_quantity=None):
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

            save_products(products)
            print(f"Product ID {product_id} updated successfully.")
            return True

    print(f"Error: Product with ID {product_id} not found.")
    return False


# ---------------------------------------------------------------------
# DELETE
# ---------------------------------------------------------------------
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


# ---------------------------------------------------------------------
# Simple menu for testing this module on its own
# ---------------------------------------------------------------------
def main():
    while True:
        print("\n--- Product Management Menu ---")
        print("1. Add Product")
        print("2. View All Products")
        print("3. Update Product")
        print("4. Delete Product")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            pid = input("Product ID: ")
            name = input("Name: ")
            price = input("Price: ")
            stock = input("Stock Quantity: ")
            add_product(pid, name, price, stock)

        elif choice == "2":
            view_all_products()

        elif choice == "3":
            pid = input("Product ID to update: ")
            name = input("New name (leave blank to skip): ") or None
            price = input("New price (leave blank to skip): ") or None
            stock = input("New stock quantity (leave blank to skip): ") or None
            update_product(pid, name, price, stock)

        elif choice == "4":
            pid = input("Product ID to delete: ")
            delete_product(pid)

        elif choice == "5":
            print("Exiting Product Management Module.")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()