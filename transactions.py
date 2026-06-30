"""
Transaction & Calculation Engine
-------------------------------------
Handles the checkout process: selecting a customer, building a cart of
products, validating stock, reducing stock after a sale, calculating
totals/discounts, and generating a receipt record.

This module is designed to plug into the rest of the group project:
    - products.py   -> Person 2/3's product & inventory module
    - customers.py  -> Person 1's customer management module

Each sale is stored as a dictionary with the keys:
    id, customer_id, customer_name, items, subtotal,
    discount_percent, discount_amount, total, timestamp

Each item inside "items" is a dictionary with the keys:
    product_id, name, unit_price, quantity, subtotal
"""

import json
import os
from datetime import datetime

import products                 
from customers import find_customer       # Person 1's module (customers)

SALES_FILE = "sales.json"


# ---------------------------------------------------------------------
# File handling helpers (same pattern as products.py / transactions.py)
# ---------------------------------------------------------------------
def load_sales():
    """Load the list of past sales/receipts from the data file."""
    if not os.path.exists(SALES_FILE):
        return []
    try:
        with open(SALES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_sales(sales):
    """Save the list of sales/receipts back to the data file."""
    with open(SALES_FILE, "w", encoding="utf-8") as f:
        json.dump(sales, f, indent=4)


def generate_sale_id(sales):
    return f"S{len(sales) + 1:04d}"


# ---------------------------------------------------------------------
# CART BUILDING
# ---------------------------------------------------------------------
def add_to_cart(cart, product_id, quantity):
    """
    Add a product + quantity to an in-progress cart (a plain list).
    Validates that the product exists and that enough stock is available.
    If the product is already in the cart, increases its quantity instead
    of adding a duplicate line. Returns True/False.
    """
    if quantity <= 0:
        print("Error: Quantity must be greater than zero.")
        return False

    product = products.get_product_by_id(product_id)
    if not product:
        print(f"Error: Product with ID {product_id} not found.")
        return False

    # If this product is already in the cart, combine quantities
    for item in cart:
        if item["product_id"] == product_id:
            new_quantity = item["quantity"] + quantity
            if not products.check_stock(product_id, new_quantity):
                print(
                    f"Error: Only {product['stock_quantity']} units of "
                    f"'{product['name']}' available."
                )
                return False
            item["quantity"] = new_quantity
            item["subtotal"] = round(item["unit_price"] * new_quantity, 2)
            return True

    # New line item
    if not products.check_stock(product_id, quantity):
        print(
            f"Error: Only {product['stock_quantity']} units of "
            f"'{product['name']}' available."
        )
        return False

    cart.append({
        "product_id": product_id,
        "name": product["name"],
        "unit_price": product["price"],
        "quantity": quantity,
        "subtotal": round(product["price"] * quantity, 2),
    })
    print(f"Added {quantity} x '{product['name']}' to cart.")
    return True


def remove_from_cart(cart, product_id):
    """Remove a product line entirely from the cart. Returns True/False."""
    for item in cart:
        if item["product_id"] == product_id:
            cart.remove(item)
            print(f"Removed '{item['name']}' from cart.")
            return True
    print(f"Error: Product ID {product_id} not in cart.")
    return False


def view_cart(cart):
    """Print the current contents of the cart in a readable table."""
    if not cart:
        print("Cart is empty.")
        return

    print(f"{'Product':<20}{'Unit Price':<12}{'Qty':<6}{'Subtotal':<10}")
    print("-" * 48)
    for item in cart:
        print(
            f"{item['name']:<20}"
            f"{item['unit_price']:<12.2f}"
            f"{item['quantity']:<6}"
            f"{item['subtotal']:<10.2f}"
        )


# ---------------------------------------------------------------------
# CALCULATION ALGORITHMS
# ---------------------------------------------------------------------
def calculate_subtotal(cart):
    """Sum the subtotal of every line item in the cart."""
    return round(sum(item["subtotal"] for item in cart), 2)


def apply_discount(subtotal, discount_percent=None):
    """
    Work out the discount to apply to an order.

    If discount_percent is given explicitly (e.g. a staff override or a
    promo code), that value is used. Otherwise, an automatic tiered
    discount is applied based on order size:
        subtotal >= 10000  -> 10% off
        subtotal >= 5000   -> 5% off
        otherwise          -> 0% off

    Returns a tuple: (discount_amount, discount_percent_used)
    """
    if discount_percent is None:
        if subtotal >= 10000:
            discount_percent = 10
        elif subtotal >= 5000:
            discount_percent = 5
        else:
            discount_percent = 0

    discount_amount = round(subtotal * (discount_percent / 100), 2)
    return discount_amount, discount_percent


def calculate_total(subtotal, discount_amount):
    """Final amount payable after discount."""
    return round(subtotal - discount_amount, 2)


# ---------------------------------------------------------------------
# CORE CHECKOUT PROCESS
# ---------------------------------------------------------------------
def process_sale(customer_id, cart, discount_percent=None):
    """
    Process a complete sale:
        1. Validate the customer exists.
        2. Validate the cart is not empty.
        3. Validate stock availability for every item BEFORE changing anything.
        4. Reduce stock for every item.
        5. Calculate subtotal, discount, and total.
        6. Build and save a receipt record.

    Returns the receipt dict on success, or None if the sale was rejected.
    """
    customer = find_customer(customer_id)
    if not customer:
        print(f"Error: Customer with ID {customer_id} not found.")
        return None

    if not cart:
        print("Error: Cannot process a sale with an empty cart.")
        return None

    # Step 1: validate stock for ALL items first, so we never reduce stock
    # for some items and then fail halfway through on another item.
    for item in cart:
        if not products.check_stock(item["product_id"], item["quantity"]):
            print(
                f"Error: Insufficient stock for '{item['name']}'. "
                f"Sale cancelled — no stock was changed."
            )
            return None

    # Step 2: all checks passed, now actually reduce stock
    for item in cart:
        products.reduce_stock(item["product_id"], item["quantity"])

    # Step 3: run the calculations
    subtotal = calculate_subtotal(cart)
    discount_amount, discount_percent_used = apply_discount(subtotal, discount_percent)
    total = calculate_total(subtotal, discount_amount)

    # Step 4: build the receipt record
    sales = load_sales()
    receipt = {
        "id": generate_sale_id(sales),
        "customer_id": customer["id"],
        "customer_name": customer["name"],
        "items": cart,
        "subtotal": subtotal,
        "discount_percent": discount_percent_used,
        "discount_amount": discount_amount,
        "total": total,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    sales.append(receipt)
    save_sales(sales)

    print(f"\nSale {receipt['id']} completed successfully for {customer['name']}.")
    return receipt


# ---------------------------------------------------------------------
# RECEIPT DISPLAY / LOOKUP
# ---------------------------------------------------------------------
def print_receipt(receipt):
    """Print a formatted receipt to the console."""
    print("\n" + "=" * 40)
    print(f"RECEIPT  #{receipt['id']}")
    print("=" * 40)
    print(f"Customer: {receipt['customer_name']} ({receipt['customer_id']})")
    print(f"Date:     {receipt['timestamp']}")
    print("-" * 40)
    print(f"{'Item':<18}{'Qty':<5}{'Price':<8}{'Subtotal':<9}")
    for item in receipt["items"]:
        print(
            f"{item['name']:<18}"
            f"{item['quantity']:<5}"
            f"{item['unit_price']:<8.2f}"
            f"{item['subtotal']:<9.2f}"
        )
    print("-" * 40)
    print(f"{'Subtotal:':<31}{receipt['subtotal']:>9.2f}")
    print(f"{'Discount (' + str(receipt['discount_percent']) + '%):':<31}"
          f"{receipt['discount_amount']:>9.2f}")
    print(f"{'TOTAL:':<31}{receipt['total']:>9.2f}")
    print("=" * 40)


def find_sale(sale_id):
    """Return a single sale/receipt dict by ID, or None if not found."""
    sales = load_sales()
    for sale in sales:
        if sale["id"] == sale_id:
            return sale
    return None


def view_all_sales():
    """Display a summary table of every past sale."""
    sales = load_sales()
    if not sales:
        print("No sales recorded yet.")
        return

    print(f"{'ID':<7}{'Customer':<20}{'Total':<10}{'Date':<20}")
    print("-" * 57)
    for sale in sales:
        print(
            f"{sale['id']:<7}"
            f"{sale['customer_name']:<20}"
            f"{sale['total']:<10.2f}"
            f"{sale['timestamp']:<20}"
        )


# ---------------------------------------------------------------------
# Simple menu for testing this module on its own
# ---------------------------------------------------------------------
def main():
    while True:
        print("\n--- Sales / Checkout Menu ---")
        print("1. Process New Sale")
        print("2. View All Sales")
        print("3. View Receipt by ID")
        print("4. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            customer_id = input("Customer ID: ")
            cart = []
            while True:
                print("\nCurrent cart:")
                view_cart(cart)
                print("\na) Add product   d) Done adding   c) Cancel sale")
                step = input("Choice: ").strip().lower()

                if step == "a":
                    pid = input("Product ID: ")
                    try:
                        qty = int(input("Quantity: "))
                    except ValueError:
                        print("Error: Quantity must be a whole number.")
                        continue
                    add_to_cart(cart, pid, qty)

                elif step == "d":
                    break

                elif step == "c":
                    cart = []
                    print("Sale cancelled.")
                    break

                else:
                    print("Invalid choice. Try again.")

            if cart:
                override = input(
                    "Manual discount % (leave blank for automatic): "
                ).strip()
                discount_percent = float(override) if override else None
                receipt = process_sale(customer_id, cart, discount_percent)
                if receipt:
                    print_receipt(receipt)

        elif choice == "2":
            view_all_sales()

        elif choice == "3":
            sid = input("Sale ID: ")
            sale = find_sale(sid)
            if sale:
                print_receipt(sale)
            else:
                print(f"Error: Sale with ID {sid} not found.")

        elif choice == "4":
            print("Exiting Sales / Checkout Module.")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()