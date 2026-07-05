"""Utility algorithms for sorting, searching, and sales analytics."""


def linear_search_by_id(items, item_id, key="id"):
    """Return the first dictionary in items with key == item_id, else None."""
    for item in items:
        if item.get(key) == item_id:
            return item
    return None


def sort_dicts_by_key(items, key, reverse=False):
    """Return a sorted copy of a list of dictionaries by a given key."""
    return sorted(items, key=lambda x: x.get(key, 0), reverse=reverse)


def sort_products(products, by="name", reverse=False):
    """Sort products by name, price, or stock_quantity and return a new list."""
    valid_keys = {"name", "price", "stock_quantity"}
    if by not in valid_keys:
        raise ValueError(f"Invalid sort key: {by}. Use one of {sorted(valid_keys)}")

    if by == "name":
        return sorted(products, key=lambda p: str(p.get("name", "")).lower(), reverse=reverse)

    return sorted(products, key=lambda p: p.get(by, 0), reverse=reverse)


def calculate_total_revenue(sales):
    """Return total revenue from a list of sales records."""
    return round(sum(sale.get("total", 0) for sale in sales), 2)


def calculate_average_sale(sales):
    """Return average sale value, 0 if there are no sales."""
    if not sales:
        return 0.0
    return round(calculate_total_revenue(sales) / len(sales), 2)


def top_selling_products(sales, top_n=5):
    """Return list of tuples (product_id, product_name, total_quantity_sold)."""
    product_totals = {}

    for sale in sales:
        for item in sale.get("items", []):
            pid = item.get("product_id")
            name = item.get("name", "Unknown")
            qty = item.get("quantity", 0)

            if pid not in product_totals:
                product_totals[pid] = {
                    "name": name,
                    "quantity": 0,
                }

            product_totals[pid]["quantity"] += qty

    ranked = sorted(
        product_totals.items(),
        key=lambda kv: kv[1]["quantity"],
        reverse=True,
    )

    result = []
    for pid, data in ranked[:top_n]:
        result.append((pid, data["name"], data["quantity"]))

    return result


def sales_per_customer(sales):
    """Return a dictionary mapping customer_id to number of sales."""
    counts = {}
    for sale in sales:
        cid = sale.get("customer_id")
        counts[cid] = counts.get(cid, 0) + 1
    return counts
