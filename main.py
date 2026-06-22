# main.py
# ==========================================
# MEMBER 6: USER INTERFACE (CLI) & INTEGRATION LEAD
# ==========================================

# --- MOCK DATA FOR EARLY INTEGRATION TESTING ---
# (Once Member 5 finishes file handling, these will be replaced by actual file loads)
mock_products = [
    {"ID": "P001", "Name": "Laptop", "Price": "1200.00", "Stock": "3"},  # Low stock
    {"ID": "P002", "Name": "Mouse", "Price": "25.00", "Stock": "50"},
    {"ID": "P003", "Name": "Keyboard", "Price": "45.00", "Stock": "2"}, # Low stock
]

mock_sales = [
    {"Sale_ID": "S0001", "Customer_ID": "C001", "Product_ID": "P001", "Quantity": "1", "Total_Price": "1200.00"},
    {"Sale_ID": "S0002", "Customer_ID": "C002", "Product_ID": "P002", "Quantity": "2", "Total_Price": "50.00"},
]

# --- PEER MODULE PLACEHOLDERS ---
def placeholder_product_menu():
    print("\n[!] Member 1's Product Management Module will launch here.")

def placeholder_customer_menu():
    print("\n[!] Member 2's Customer Module will launch here.")

def placeholder_transaction_menu():
    print("\n[!] Member 3's Transaction Module (Checkout) will launch here.")


# ==========================================
# MEMBER 6 CORE DELIVERABLE: REPORTS ENGINE
# ==========================================
def generate_sales_report():
    print("\n=========================================")
    print("         SYSTEM PERFORMANCE REPORT       ")
    print("=========================================")
    
    # 1. Calculate totals and summaries using data metrics [cite: 6]
    total_revenue = 0.0
    for sale in mock_sales:
        total_revenue += float(sale["Total_Price"])
        
    print(f"Total Gross Revenue: ${total_revenue:.2f}")
    print(f"Total Transactions Processed: {len(mock_sales)}")
    print("-----------------------------------------")
    
    # 2. Display Low-Stock Alerts (Validates availability) [cite: 5]
    print("⚠️  CRITICAL LOW-STOCK ALERTS:")
    low_stock_threshold = 5
    low_stock_found = False
    
    for product in mock_products:
        current_stock = int(product["Stock"])
        if current_stock < low_stock_threshold:
            print(f"  ❌ ITEM CRITICAL: {product['Name']} (ID: {product['ID']}) | Only {current_stock} left!")
            low_stock_found = True
            
    if not low_stock_found:
        print("  ✅ All inventory stock levels are healthy.")
    print("=========================================")


# ==========================================
# MEMBER 6 CORE DELIVERABLE: MAIN MENU (CLI)
# ==========================================
def main_menu():
    while True:
        print("\n" + "="*45)
        print("     SALES MANAGEMENT SYSTEM - MENU      ")
        print("=========================================")
        print("1. Manage Products       (Member 1)")
        print("2. Manage Customers      (Member 2)")
        print("3. Process New Sale      (Member 3)")
        print("4. View Reports & Alerts (Member 6)")
        print("5. Exit System")
        print("=========================================")
        
        choice = input("Select an option (1-5): ").strip()
        
        if choice == '1':
            placeholder_product_menu()
        elif choice == '2':
            placeholder_customer_menu()
        elif choice == '3':
            placeholder_transaction_menu()
        elif choice == '4':
            generate_sales_report()
        elif choice == '5':
            print("\nShutting down integration engine safely... Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please select a number from 1 to 5.")

if __name__ == "__main__":
    main_menu()