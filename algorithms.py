"""Utility algorithms for sorting, searching, and sales analytics."""


def _merge(left, right, key_func, reverse=False):
    """Merge two sorted lists into one sorted list while preserving stability."""
    merged = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        left_key = key_func(left[i])
        right_key = key_func(right[j])

        if reverse:
            # For descending order, keep left-side precedence on equal keys.
            take_left = left_key >= right_key
        else:
            # For ascending order, keep left-side precedence on equal keys.
            take_left = left_key <= right_key

        if take_left:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    if i < len(left):
        merged.extend(left[i:])
    if j < len(right):
        merged.extend(right[j:])

    return merged


def merge_sort(items, key_func=lambda x: x, reverse=False):
    """Return a sorted copy of items using merge sort."""
    items_copy = list(items)
    if len(items_copy) <= 1:
        return items_copy

    mid = len(items_copy) // 2
    left = merge_sort(items_copy[:mid], key_func=key_func, reverse=reverse)
    right = merge_sort(items_copy[mid:], key_func=key_func, reverse=reverse)
    return _merge(left, right, key_func=key_func, reverse=reverse)


def linear_search_by_id(items, item_id, key="id"):
    """Return the first dictionary in items with key == item_id, else None."""
    for item in items:
        if item.get(key) == item_id:
            return item
    return None


def sort_dicts_by_key(items, key, reverse=False):
    """Return a sorted copy of a list of dictionaries by a given key."""
    return merge_sort(items, key_func=lambda x: x.get(key, 0), reverse=reverse)


def sort_products(products, by="name", reverse=False):
    """Sort products by name, price, or stock_quantity and return a new list."""
    # Keep sort options explicit to avoid silently sorting by unsupported fields.
    valid_keys = {"name", "price", "stock_quantity"}
    if by not in valid_keys:
        valid_keys_ordered = ["name", "price", "stock_quantity"]
        raise ValueError(f"Invalid sort key: {by}. Use one of {valid_keys_ordered}")

    if by == "name":
        return merge_sort(
            products,
            key_func=lambda p: str(p.get("name", "")).lower(),
            reverse=reverse,
        )

    return merge_sort(products, key_func=lambda p: p.get(by, 0), reverse=reverse)


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

    # Rank aggregated quantities in descending order.
    ranked = merge_sort(
        product_totals.items(),
        key_func=lambda kv: kv[1]["quantity"],
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
