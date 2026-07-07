"""Reporting module for sales, inventory, and customers."""

import csv
import os

import algorithms
import customers
import products
import transactions


# High-level KPI summary over the full sales dataset.
def sales_summary_report():
    """Print summary stats from all recorded sales."""
    sales = transactions.load_sales()

    if not sales:
        print("No sales data available.")
        return

    total_sales = len(sales)
    total_revenue = algorithms.calculate_total_revenue(sales)
    average_sale = algorithms.calculate_average_sale(sales)
    best_sale = max(sales, key=lambda s: s.get("total", 0))

    print("\n=== Sales Summary Report ===")
    print(f"Total Transactions: {total_sales}")
    print(f"Total Revenue:      {total_revenue:.2f}")
    print(f"Average Sale:       {average_sale:.2f}")
    print(f"Highest Sale:       {best_sale.get('id')} ({best_sale.get('total', 0):.2f})")


def low_stock_report(threshold=5):
    """Print products with stock quantity below or equal to threshold."""
    low_stock_items = products.get_low_stock_products(threshold)

    print(f"\n=== Low Stock Report (threshold <= {threshold}) ===")
    if not low_stock_items:
        print("No products are currently low in stock.")
        return

    print(f"{'ID':<6}{'Name':<20}{'Stock':<10}{'Category':<15}")
    print("-" * 51)
    for item in low_stock_items:
        print(
            f"{item.get('id', ''):<6}"
            f"{item.get('name', ''):<20}"
            f"{item.get('stock_quantity', 0):<10}"
            f"{(item.get('category') or ''):<15}"
        )


def top_products_report(top_n=5):
    """Print top-selling products from sales history."""
    sales = transactions.load_sales()
    top_items = algorithms.top_selling_products(sales, top_n=top_n)

    print(f"\n=== Top {top_n} Selling Products ===")
    if not top_items:
        print("No sales data available to rank products.")
        return

    print(f"{'Product ID':<12}{'Name':<22}{'Qty Sold':<10}")
    print("-" * 44)
    for pid, name, qty in top_items:
        print(f"{pid:<12}{name:<22}{qty:<10}")


def customer_activity_report():
    """Print each customer and how many transactions they have."""
    sales = transactions.load_sales()
    all_customers = customers.load_customers()
    counts = algorithms.sales_per_customer(sales)

    print("\n=== Customer Activity Report ===")
    if not all_customers:
        print("No customers found.")
        return

    print(f"{'Customer ID':<12}{'Name':<22}{'Transactions':<12}")
    print("-" * 46)
    for customer in all_customers:
        cid = customer.get("id")
        print(f"{cid:<12}{customer.get('name', ''):<22}{counts.get(cid, 0):<12}")


def sorted_inventory_report(sort_by="name", descending=False):
    """Print products sorted by name, price, or stock quantity."""
    inventory = products.load_products()

    print(f"\n=== Inventory Sorted by {sort_by} ({'DESC' if descending else 'ASC'}) ===")
    if not inventory:
        print("No products found.")
        return

    try:
        sorted_inventory = algorithms.sort_products(inventory, by=sort_by, reverse=descending)
    except ValueError as exc:
        print(f"Error: {exc}")
        return

    print(f"{'ID':<6}{'Name':<20}{'Price':<10}{'Stock':<10}{'Category':<15}")
    print("-" * 61)
    for item in sorted_inventory:
        print(
            f"{item.get('id', ''):<6}"
            f"{item.get('name', ''):<20}"
            f"{item.get('price', 0):<10.2f}"
            f"{item.get('stock_quantity', 0):<10}"
            f"{(item.get('category') or ''):<15}"
        )


def export_sales_csv(output_path="data/sales_report.csv"):
    """Export flat sales lines to CSV for spreadsheet analysis."""
    sales = transactions.load_sales()
    if not sales:
        print("No sales data to export.")
        return False

    directory = os.path.dirname(output_path)
    if directory:
        os.makedirs(directory, exist_ok=True)

    # Flatten nested sale items so each row is import-friendly for spreadsheet tools.
    with open(output_path, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = [
            "sale_id",
            "timestamp",
            "customer_id",
            "customer_name",
            "product_id",
            "product_name",
            "quantity",
            "unit_price",
            "line_subtotal",
            "sale_total",
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for sale in sales:
            for item in sale.get("items", []):
                writer.writerow(
                    {
                        "sale_id": sale.get("id"),
                        "timestamp": sale.get("timestamp"),
                        "customer_id": sale.get("customer_id"),
                        "customer_name": sale.get("customer_name"),
                        "product_id": item.get("product_id"),
                        "product_name": item.get("name"),
                        "quantity": item.get("quantity"),
                        "unit_price": item.get("unit_price"),
                        "line_subtotal": item.get("subtotal"),
                        "sale_total": sale.get("total"),
                    }
                )

    print(f"Sales CSV exported to: {output_path}")
    return True


def reports_menu():
    """Simple menu to run all report functions."""
    # Interactive entry point for report generation from the CLI app.
    while True:
        print("\n--- Reports Menu ---")
        print("1. Sales Summary")
        print("2. Low Stock Report")
        print("3. Top-Selling Products")
        print("4. Customer Activity")
        print("5. Export Sales CSV")
        print("6. Sorted Inventory")
        print("7. Back to Main Menu")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            sales_summary_report()
        elif choice == "2":
            raw = input("Low-stock threshold (default 5): ").strip()
            threshold = int(raw) if raw else 5
            low_stock_report(threshold)
        elif choice == "3":
            raw = input("How many top products? (default 5): ").strip()
            top_n = int(raw) if raw else 5
            top_products_report(top_n)
        elif choice == "4":
            customer_activity_report()
        elif choice == "5":
            path = input("Output CSV path (default data/sales_report.csv): ").strip()
            export_sales_csv(path or "data/sales_report.csv")
        elif choice == "6":
            print("Sort by: name, price, stock_quantity")
            sort_by = input("Sort key (default name): ").strip() or "name"
            order = input("Descending order? (y/N): ").strip().lower()
            sorted_inventory_report(sort_by=sort_by, descending=(order == "y"))
        elif choice == "7":
            break
        else:
            print("Invalid choice. Try again.")
