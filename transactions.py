"""
Customer Management Module
-------------------------------------
Handles management of customer records: adding, viewing, updating,
and removing customer profiles.

Each customer is stored as a dictionary with the keys:
    id, name, contact_info


This keeps the CRUD logic completely separate from how the file is
actually stored, so the modules from different people can be merged
easily later.
"""

import json
import os

DATA_FILE = "customers.json"


# ---------------------------------------------------------------------
# File handling helpers 

# ---------------------------------------------------------------------
def load_customers():
    """Load the list of customers from the data file."""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_customers(customers):
    """Save the list of customers back to the data file."""
    with open(DATA_FILE, "w") as f:
        json.dump(customers, f, indent=4)


# ---------------------------------------------------------------------
# CREATE
# ---------------------------------------------------------------------
def add_customer(customer_id, name, contact_info):
    """Add a new customer. Returns True on success, False if ID already exists."""
    customers = load_customers()

    for customer in customers:
        if customer["id"] == customer_id:
            print(f"Error: Customer with ID {customer_id} already exists.")
            return False

    new_customer = {
        "id": customer_id,
        "name": name,
        "contact_info": contact_info,
    }
    customers.append(new_customer)
    save_customers(customers)
    print(f"Customer '{name}' added successfully.")
    return True


# ---------------------------------------------------------------------
# READ
# ---------------------------------------------------------------------
def view_all_customers():
    """Display all customers in a readable table format."""
    customers = load_customers()

    if not customers:
        print("No customers found.")
        return

    print(f"{'ID':<6}{'Name':<20}{'Contact Info':<25}")
    print("-" * 51)
    for customer in customers:
        print(
            f"{customer['id']:<6}{customer['name']:<20}{customer['contact_info']:<25}"
        )


def find_customer(customer_id):
    """Return a single customer dict by ID, or None if not found."""
    customers = load_customers()
    for customer in customers:
        if customer["id"] == customer_id:
            return customer
    return None


# ---------------------------------------------------------------------
# UPDATE
# ---------------------------------------------------------------------
def update_customer(customer_id, name=None, contact_info=None):
    """Update one or more fields of an existing customer. Returns True/False."""
    customers = load_customers()

    for customer in customers:
        if customer["id"] == customer_id:
            if name is not None:
                customer["name"] = name
            if contact_info is not None:
                customer["contact_info"] = contact_info

            save_customers(customers)
            print(f"Customer ID {customer_id} updated successfully.")
            return True

    print(f"Error: Customer with ID {customer_id} not found.")
    return False


# ---------------------------------------------------------------------
# DELETE
# ---------------------------------------------------------------------
def delete_customer(customer_id):
    """Remove a customer by ID. Returns True if deleted, False if not found."""
    customers = load_customers()
    updated_customers = [c for c in customers if c["id"] != customer_id]

    if len(updated_customers) == len(customers):
        print(f"Error: Customer with ID {customer_id} not found.")
        return False

    save_customers(updated_customers)
    print(f"Customer ID {customer_id} removed successfully.")
    return True


# ---------------------------------------------------------------------
# Simple menu for testing this module on its own
# ---------------------------------------------------------------------
def main():
    while True:
        print("\n--- Customer Management Menu ---")
        print("1. Add Customer")
        print("2. View All Customers")
        print("3. Update Customer")
        print("4. Remove Customer")
        print("5. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            cid = input("Customer ID: ")
            name = input("Name: ")
            contact = input("Contact Info: ")
            add_customer(cid, name, contact)

        elif choice == "2":
            view_all_customers()

        elif choice == "3":
            cid = input("Customer ID to update: ")
            name = input("New name (leave blank to skip): ") or None
            contact = input("New contact info (leave blank to skip): ") or None
            update_customer(cid, name, contact)

        elif choice == "4":
            cid = input("Customer ID to remove: ")
            delete_customer(cid)

        elif choice == "5":
            print("Exiting Customer Management Module.")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()