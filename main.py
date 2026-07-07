"""Main entry point for the sales management system."""

import customers
import products
import reports
import transactions


def products_menu():
    # Delegate product CRUD operations to the products module.
    while True:
        print("\n--- Products Menu ---")
        print("1. Add Product")
        print("2. View Products")
        print("3. Update Product")
        print("4. Delete Product")
        print("5. Back")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            pid = input("Product ID (leave blank to auto-generate): ").strip()
            if not pid:
                pid = products.generate_product_id(products.load_products())

            name = input("Name: ").strip()
            price = input("Price: ").strip()
            stock = input("Stock quantity: ").strip()
            category = input("Category (optional): ").strip() or None

            try:
                products.add_product(pid, name, float(price), int(stock), category)
            except ValueError:
                print("Error: Price must be a number and stock must be a whole number.")

        elif choice == "2":
            products.view_all_products()

        elif choice == "3":
            pid = input("Product ID to update: ").strip()
            name = input("New name (blank to skip): ").strip() or None
            price_raw = input("New price (blank to skip): ").strip()
            stock_raw = input("New stock qty (blank to skip): ").strip()
            category = input("New category (blank to skip): ").strip() or None

            price = None
            stock = None

            try:
                if price_raw:
                    price = float(price_raw)
                if stock_raw:
                    stock = int(stock_raw)
            except ValueError:
                print("Error: Invalid numeric input.")
                continue

            products.update_product(pid, name=name, price=price, stock_quantity=stock, category=category)

        elif choice == "4":
            pid = input("Product ID to delete: ").strip()
            products.delete_product(pid)

        elif choice == "5":
            break

        else:
            print("Invalid choice. Try again.")


def customers_menu():
    # Delegate customer CRUD operations to the customers module.
    while True:
        print("\n--- Customers Menu ---")
        print("1. Add Customer")
        print("2. View Customers")
        print("3. Update Customer")
        print("4. Delete Customer")
        print("5. Back")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            cid = input("Customer ID: ").strip()
            name = input("Name: ").strip()
            contact = input("Contact info: ").strip()
            customers.add_customer(cid, name, contact)

        elif choice == "2":
            customers.view_all_customers()

        elif choice == "3":
            cid = input("Customer ID to update: ").strip()
            name = input("New name (blank to skip): ").strip() or None
            contact = input("New contact info (blank to skip): ").strip() or None
            customers.update_customer(cid, name=name, contact_info=contact)

        elif choice == "4":
            cid = input("Customer ID to delete: ").strip()
            customers.delete_customer(cid)

        elif choice == "5":
            break

        else:
            print("Invalid choice. Try again.")


def main_menu():
    # Top-level router for all application workflows.
    while True:
        print("\n========== Sales Management System ==========")
        print("1. Manage Products")
        print("2. Manage Customers")
        print("3. Process Transactions")
        print("4. Reports")
        print("5. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            products_menu()
        elif choice == "2":
            customers_menu()
        elif choice == "3":
            transactions.main()
        elif choice == "4":
            reports.reports_menu()
        elif choice == "5":
            print("Goodbye.")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main_menu()
