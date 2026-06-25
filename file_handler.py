import csv
import os

# ──────────────────────────────────────────────
# FILE PATHS 
# ──────────────────────────────────────────────
DATA_FOLDER = "data"
PRODUCTS_FILE    = os.path.join(DATA_FOLDER, "products.csv")
CUSTOMERS_FILE   = os.path.join(DATA_FOLDER, "customers.csv")
TRANSACTIONS_FILE = os.path.join(DATA_FOLDER, "transactions.csv")

# Column headers 
PRODUCT_FIELDS     = ["id", "name", "price", "stock"]
CUSTOMER_FIELDS    = ["id", "name", "phone"]
TRANSACTION_FIELDS = ["id", "customer_id", "product_id", "quantity", "total", "date"]


def _ensure_data_folder():
    """Creates the data/ folder if it doesn't exist."""
    os.makedirs(DATA_FOLDER, exist_ok=True)


# ══════════════════════════════════════════════
# PRODUCTS
# ══════════════════════════════════════════════

def load_products() -> list[dict]:
    """
    Loads products from CSV and returns a clean list of dicts.
    Each dict: {"id": str, "name": str, "price": float, "stock": int}
    Returns [] if file doesn't exist yet.
    """
    if not os.path.exists(PRODUCTS_FILE):
        return []
    try:
        with open(PRODUCTS_FILE, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            products = []
            for row in reader:
                products.append({
                    "id":    row["id"],
                    "name":  row["name"],
                    "price": float(row["price"]),   # convert string → float
                    "stock": int(row["stock"])       # convert string → int
                })
            return products
    except (FileNotFoundError, KeyError, ValueError) as e:
        print(f"[FileHandler] Error loading products: {e}")
        return []


def save_products(products: list[dict]) -> bool:
    """
    Saves a list of product dicts to CSV.
    Returns True on success, False on failure.
    """
    _ensure_data_folder()
    try:
        with open(PRODUCTS_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=PRODUCT_FIELDS)
            writer.writeheader()
            writer.writerows(products)
        return True
    except IOError as e:
        print(f"[FileHandler] Error saving products: {e}")
        return False


# ══════════════════════════════════════════════
# CUSTOMERS
# ══════════════════════════════════════════════

def load_customers() -> list[dict]:
    """
    Loads customers from CSV.
    Each dict: {"id": str, "name": str, "phone": str}
    """
    if not os.path.exists(CUSTOMERS_FILE):
        return []
    try:
        with open(CUSTOMERS_FILE, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return [{"id": r["id"], "name": r["name"], "phone": r["phone"]}
                    for r in reader]
    except (FileNotFoundError, KeyError) as e:
        print(f"[FileHandler] Error loading customers: {e}")
        return []


def save_customers(customers: list[dict]) -> bool:
    """Saves a list of customer dicts to CSV."""
    _ensure_data_folder()
    try:
        with open(CUSTOMERS_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CUSTOMER_FIELDS)
            writer.writeheader()
            writer.writerows(customers)
        return True
    except IOError as e:
        print(f"[FileHandler] Error saving customers: {e}")
        return False


# ══════════════════════════════════════════════
# TRANSACTIONS
# ══════════════════════════════════════════════

def load_transactions() -> list[dict]:
    """
    Loads transactions from CSV.
    Each dict: {"id", "customer_id", "product_id", "quantity": int,
                "total": float, "date": str}
    """
    if not os.path.exists(TRANSACTIONS_FILE):
        return []
    try:
        with open(TRANSACTIONS_FILE, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            transactions = []
            for row in reader:
                transactions.append({
                    "id":          row["id"],
                    "customer_id": row["customer_id"],
                    "product_id":  row["product_id"],
                    "quantity":    int(row["quantity"]),
                    "total":       float(row["total"]),
                    "date":        row["date"]
                })
            return transactions
    except (FileNotFoundError, KeyError, ValueError) as e:
        print(f"[FileHandler] Error loading transactions: {e}")
        return []


def save_transactions(transactions: list[dict]) -> bool:
    """Saves a list of transaction dicts to CSV."""
    _ensure_data_folder()
    try:
        with open(TRANSACTIONS_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=TRANSACTION_FIELDS)
            writer.writeheader()
            writer.writerows(transactions)
        return True
    except IOError as e:
        print(f"[FileHandler] Error saving transactions: {e}")
        return False