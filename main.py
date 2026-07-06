# main.py
# ==========================================
# MEMBER 6: USER INTERFACE (CLI) & INTEGRATION LEAD
# ==========================================

# 1. IMPORT YOUR TEAMMATES' WORK LIVE
try:
    import product_module      # Member 1 & 2's CRUD features
    import customer_module     # Member 3's Customer Module
    import transaction_module  # Member 4's Checkout Engine
    import file_handling       # Member 5's Database Engine
except ImportError as e:
    print(f"⚠️ Integration Warning: Could not import a module ({e}).")
    print("Ensure all your teammates' .py files are in this same folder.")


# ==========================================
# MEMBER 6 CORE DELIVERABLE: REPORTS ENGINE
# ==========================================
def generate_sales_report():
    print("\n=========================================")
    print("         SYSTEM PERFORMANCE REPORT       ")
    print("=========================================")
    
    try:
        # Load live database tracking array matrices
        sales = file_handling.read_file("sales.txt") 
        products = file_handling.read_file("products.txt")
    except NameError:
        print("❌ Error: file_handling module is missing or incomplete.")
        return
    
    if not sales:
        print("No transactions recorded yet.")
        print("-----------------------------------------")
    else:
        # 1. Calculate live financial aggregates
        total_revenue = 0.0
        for sale in sales:
            total_revenue += float(sale.get("Total_Price", 0) or 0)
            
        print(f"Total Gross Revenue: ${total_revenue:.2f}")
        print(f"Total Transactions Processed: {len(sales)}")
        print("-----------------------------------------")
    
    # 2. Live Low-Stock Alerts (Validates inventory availability thresholds)
    print("⚠️  CRITICAL LOW-STOCK ALERTS:")
    low_stock_threshold = 5
    low_stock_found = False
    
    if products:
        for product in products:
            current_stock = int(product.get("Stock", 0) or 0)
            if current_stock < low_stock_threshold:
                print(f"  ❌ ITEM CRITICAL: {product.get('Name', 'Unknown')} (ID: {product.get('ID')}) | Only {current_stock} left!")
                low_stock_found = True
                
    if not low_stock_found:
        print("  ✅ All inventory stock levels are healthy.")
    print("=========================================")


# ==========================================
# MEMBER 6 CORE DELIVERABLE: MAIN MENU (CLI)
# ==========================================
def main_menu():
    # Initialize the data files on boot-up sequence
    try:
        file_handling.initialize_files()
    except NameError:
        pass
    
    while True:
        print("\n" + "="*45)
        print("     SALES MANAGEMENT SYSTEM - MENU      ")
        print("=========================================")
        print("1. Manage Products       (Member 1/2)")
        print("2. Manage Customers      (Member 3)")
        print("3. Process New Sale      (Member 4)")
        print("4. View Reports & Alerts (Member 6)")
        print("5. Exit System")
        print("=========================================")
        
        choice = input("Select an option (1-5): ").strip()
        
        if choice == '1':
            try:
                product_module.view_products() 
            except AttributeError:
                print("❌ Sub-menu function inside product_module failed to launch.")
            except NameError:
                print("❌ product_module file not found.")
        elif choice == '2':
            try:
                customer_module.view_customers()
            except AttributeError:
                print("❌ Sub-menu function inside customer_module failed to launch.")
            except NameError:
                print("❌ customer_module file not found.")
        elif choice == '3':
            try:
                transaction_module.process_sale()
            except AttributeError:
                print("❌ process_sale function inside transaction_module failed to launch.")
            except NameError:
                print("❌ transaction_module file not found.")
        elif choice == '4':
            generate_sales_report()
        elif choice == '5':
            print("\nShutting down system safely... Session complete. Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please select a number from 1 to 5.")

if __name__ == "__main__":
    main_menu()