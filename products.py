# products.py

import file_handler

PRODUCTS_FILE = "data/products.txt"

# ----------------------------

# Helper Functions

# ----------------------------

def load_products():
return file_handler.load_data(PRODUCTS_FILE)

def save_products(products):
file_handler.save_data(PRODUCTS_FILE, products)

def generate_product_id(products):
return f"P{len(products)+1:03d}"

# ----------------------------

# CRUD Operations

# ----------------------------

def add_product():
products = load_products()

```
product = {
    "id": generate_product_id(products),
    "name": input("Product Name: "),
    "price": float(input("Price: ")),
    "stock": int(input("Stock Quantity: ")),
    "category": input("Category: ")
}

products.append(product)
save_products(products)

print("Product added successfully.")
```

def view_products():
products = load_products()

```
if not products:
    print("No products available.")
    return

print("\n--- PRODUCT LIST ---")

for p in products:
    print(
        f"{p['id']} | "
        f"{p['name']} | "
        f"KES {p['price']} | "
        f"Stock: {p['stock']} | "
        f"{p['category']}"
    )
```

def search_product():
products = load_products()

```
keyword = input("Enter Product ID or Name: ").lower()

found = False

for p in products:
    if keyword in p["id"].lower() or keyword in p["name"].lower():
        print(p)
        found = True

if not found:
    print("Product not found.")
```

def update_product():
products = load_products()

```
product_id = input("Enter Product ID: ").upper()

for p in products:

    if p["id"] == product_id:

        new_name = input(f"Name [{p['name']}]: ")
        if new_name:
            p["name"] = new_name

        new_price = input(f"Price [{p['price']}]: ")
        if new_price:
            p["price"] = float(new_price)

        new_stock = input(f"Stock [{p['stock']}]: ")
        if new_stock:
            p["stock"] = int(new_stock)

        save_products(products)

        print("Product updated successfully.")
        return

print("Product not found.")
```

def delete_product():
products = load_products()

```
product_id = input("Enter Product ID: ").upper()

for p in products:

    if p["id"] == product_id:

        products.remove(p)

        save_products(products)

        print("Product deleted successfully.")
        return

print("Product not found.")
```

# ----------------------------

# Functions used by other modules

# ----------------------------

def get_product_by_id(product_id):

```
products = load_products()

for p in products:
    if p["id"] == product_id:
        return p

return None
```

def check_stock(product_id, quantity):

```
product = get_product_by_id(product_id)

if product:
    return product["stock"] >= quantity

return False
```

def reduce_stock(product_id, quantity):

```
products = load_products()

for p in products:

    if p["id"] == product_id:

        if p["stock"] < quantity:
            return False

        p["stock"] -= quantity

        save_products(products)

        return True

return False
```

def get_low_stock_products(threshold=5):

```
products = load_products()

return [p for p in products if p["stock"] <= threshold]
```
