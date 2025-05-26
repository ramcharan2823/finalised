from products import Product
from customers import Customer
from sales import Sale
from utils import input_int, input_float, confirm

def product_menu():
    product = Product()
    while True:
        print("\n--- Product Menu ---")
        print("1. Add product")
        print("2. View products")
        print("3. Update product stock")
        print("4. Delete product")
        print("5. Search product")
        print("0. Back to main menu")

        try:
            choice = input_int("Choose an option: ", 0, 5)

            if choice == 1:
                product.add_product()

            elif choice == 2:
                page = 1
                while True:
                    product.view_products(page=page)
                    nav = input("N-next page, P-previous page, Q-quit: ").lower()
                    if nav == 'n':
                        page += 1
                    elif nav == 'p' and page > 1:
                        page -= 1
                    elif nav == 'q':
                        break
                    else:
                        print("Invalid option.")

            elif choice == 3:
                    product.update_product_details()

            elif choice == 4:
                pid = input("Product ID to delete: ")
                if not product.is_product_exists(pid):
                    print(f"Product with ID {pid} does not exist.")
                    continue
                if confirm("Are you sure you want to delete this product? (y/n): "):
                    product.delete_product(pid)
                    print("Product deleted.")

            elif choice == 5:
                keyword = input("Enter search keyword: ")
                product.search_product(keyword)

            elif choice == 0:
                break

        except Exception as e:
            print(f"Error: {e}")

def customer_menu():
    customer = Customer()
    while True:
        print("\n--- Customer Menu ---")
        print("1. Add customer")
        print("2. View customers")
        print("3. Update customer")
        print("4. Delete customer")
        print("5. Search customer")
        print("0. Back to main menu")

        try:
            choice = input_int("Choose an option: ", 0, 5)

            if choice == 1:
                customer.add_customer()

            elif choice == 2:
                page = 1
                while True:
                    customer.view_customers(page=page)
                    nav = input("N-next page, P-previous page, Q-quit: ").lower()
                    if nav == 'n':
                        page += 1
                    elif nav == 'p' and page > 1:
                        page -= 1
                    elif nav == 'q':
                        break
                    else:
                        print("Invalid option.")
                

            elif choice == 3:
                customer.update_customer()

            elif choice == 4:
                cid = input("Customer ID to delete: ")
                cursor = customer.conn.cursor()
                cursor.execute("SELECT 1 FROM Customers WHERE customer_id=?", (cid,))
                if cursor.fetchone() is None:
                    print("Customer ID does not exist.")
                else:
                    if confirm("Are you sure you want to delete this customer? (y/n): "):
                        customer.delete_customer(cid)

            elif choice == 5:
                keyword = input("Enter search keyword: ")
                customer.search_customer(keyword)

            elif choice == 0:
                break

        except Exception as e:
            print(f"Error: {e}")

def sale_menu():
    sale = Sale()
    while True:
        print("\n--- Sales Menu ---")
        print("1. Record a sale")
        print("2. View sales")
        print("3. Search sales")
        print("4. Low stock products")
        print("0. Back to main menu")

        try:
            choice = input_int("Choose an option: ", 0, 4)

            if choice == 1:
                sale.record_sale()
                

            elif choice == 2:
                page = 1
                while True:
                    sale.view_sales(page=page)
                    nav = input("N-next page, P-previous page, Q-quit: ").lower()
                    if nav == 'n':
                        page += 1
                    elif nav == 'p' and page > 1:
                        page -= 1
                    elif nav == 'q':
                        break
                    else:
                        print("Invalid option.")
                

            elif choice == 3:
                keyword = input("Enter search keyword (customer name/product ID): ")
                sale.search_sales(keyword)

            elif choice == 4:
                page = 1
                while True:
                    sale.alert_low_quantity(page=page)
                    nav = input("N-next page, P-previous page, Q-quit: ").lower()
                    if nav == 'n':
                        page += 1
                    elif nav == 'p' and page > 1:
                        page -= 1
                    elif nav == 'q':
                        break
                    else:
                        print("Invalid option.")
                
                

            elif choice == 0:
                break

        except Exception as e:
            print(f"Error: {e}")

def csv_menu():
    product = Product()
    customer = Customer()
    sale = Sale()
    while True:
        print("\n--- CSV Menu ---")
        print("1. export products to csv")
        print("2. import products data from csv")
        print("3. export customers to csv")
        print("4. import customers data from csv")
        print("5. export sales to csv")
        print("0. Back to main menu")

        try:
            choice = input_int("Choose an option: ", 0, 5)

            if choice == 1:
                product.export_products_csv()
            elif choice == 2:
                filename = input("Enter CSV filename to import: ")
                product.import_products_csv(filename)
            elif choice == 3:
                customer.export_customers_csv()
            elif choice == 4:
                filename = input("Enter CSV filename to import: ")
                customer.import_customers_csv(filename)
            elif choice == 5:
                sale.export_sales_csv()
            elif choice == 0:
                break
        except Exception as e:
            print(f"Error: {e}")


def billing_reports_menu():
    sale = Sale()
    while True:
        print("\n--- Billing and Reports Menu ---")
        print("1. View daily sales summary")
        print("2. View monthly sales summary")
        print("3. get_bill_details ")
        print("0. Back to main menu")

        try:
            choice = input_int("Choose an option: ",0,3)

            if choice == 1:
                sale.daily_summary()
                
            elif choice == 2:
                sale.monthly_summary()
                
            elif choice == 3:
                sale_id = int(input("Enter the sale ID to retrieve bill details: ").strip())
                sale.get_bill_details(sale_id)
            elif choice == 0:
                break
        except Exception as e:
            print(f"Error: {e}")

def main():
    while True:
        print("\n=== Inventory Management CLI ===")
        print("1. Manage Products")
        print("2. Manage Customers")
        print("3. Manage Sales")
        print("4. Billing and Reporting")
        print("5. CSV import/export")
        print("0. Exit")

        try:
            choice = input_int("Choose an option: ", 0, 5)

            if choice == 1:
                product_menu()
            elif choice == 2:
                customer_menu()
            elif choice == 3:
                sale_menu()
            elif choice == 4:
                billing_reports_menu()
            elif choice == 5:
                csv_menu()
            elif choice == 0:
                print("Goodbye!")
                break

        except Exception as e:
            print(f"Main Menu Error: {e}")

if __name__ == "__main__":
    main()
