# main.py
# ==========================================
# MEMBER 6: USER INTERFACE (CLI) & INTEGRATION LEAD
# ==========================================

import products         # Member 1 & 2
import customers        # Member 3
import transactions     # Member 4
import file_handler     # Member 5
import algorithms       # Member 5


# ==========================================
# MEMBER 6 CORE DELIVERABLE: REPORTS ENGINE
# ==========================================
def generate_sales_report():
    print("\n=========================================")
    print("         SYSTEM PERFORMANCE REPORT       ")
    print("=========================================")
    
    # 1. Connect live to Member 5's data loaders
    try:
        sales = file_handler.load_transactions() 
        products_list = file_handler.load_products()
    except Exception as e:
        print(f"❌ Error loading files from file_handler: {e}")
        return
    
    if not sales:
        print("No transactions recorded yet.")
        print("-----------------------------------------")
    else:
        # Calculate live financial aggregates
        total_revenue = 0.0
        for sale in sales:
            # Safely get Total_Price whether it's stored as 'Total_Price' or 'total_price'
            price = sale.get("Total_Price") or sale.get("total_price") or 0
            total_revenue += float(price)
            
        print(f"Total Gross Revenue: ${total_revenue:.2f}")
        print(f"Total Transactions Processed: {len(sales)}")
        print("-----------------------------------------")
    
    # 2. Live Low-Stock Alerts (Validates inventory availability)
    print("⚠️  CRITICAL LOW-STOCK ALERTS:")
    low_stock_threshold = 5
    low_stock_found = False
    
    if products_list:
        for p in products_list:
            stock = p.get("Stock") or p.get("stock") or 0
            name = p.get("Name") or p.get("name") or "Unknown"
            p_id = p.get("ID") or p.get("id") or "N/A"
            
            if int(stock) < low_stock_threshold:
                print(f"  ❌ ITEM CRITICAL: {name} (ID: {p_id}) | Only {stock} left!")
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
            try:
                # Direct route to their product list viewer
                products.view_all_products()
            except Exception as e:
                print(f"❌ Failed to launch products interface: {e}")
                
        elif choice == '2':
            try:
                # Direct route to their customer list viewer
                customers.view_all_customers()
            except Exception as e:
                print(f"❌ Failed to launch customers interface: {e}")
                
        elif choice == '3':
            try:
                # Launches their complete transaction menu loop 
                transactions.main()
            except Exception as e:
                print(f"❌ Failed to launch transaction module: {e}")
                
        elif choice == '4':
            generate_sales_report()
            
        elif choice == '5':
            print("\nShutting down system safely... Session complete. Goodbye!")
            break
        else:
            print("❌ Invalid choice. Please select a number from 1 to 5.")

if __name__ == "__main__":
    main_menu()