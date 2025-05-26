import csv
import os
from billing import Billing
from decimal import Decimal
from datetime import datetime
from db_config import database_connection


class Sale:
    def __init__(self):
        self.conn = database_connection()
        print("Connected to database")

    def record_sale(self):
        try:
            cursor = self.conn.cursor()

            customer_id = input("Enter Customer ID: ").strip()
            cursor.execute("SELECT 1 FROM Customers WHERE customer_id=?", (customer_id,))
            if cursor.fetchone() is None:
                print("Customer ID not found.")
                return

            product_id = input("Enter Product ID: ").strip()
            cursor.execute("SELECT Price, quantity FROM Products WHERE Product_id=?", (product_id,))
            result = cursor.fetchone()
            if not result:
                print("Product not found.")
                return

            price, available_quantity = result
            price = Decimal(price)

            while True:
                quantity_input = input("Enter quantity to sell: ").strip()
                try:
                    quantity = int(quantity_input)
                    if quantity <= 0:
                        print("Quantity must be a positive integer.")
                        continue
                    if quantity > available_quantity:
                        print(f"Insufficient stock. Only {available_quantity} items available.")
                        return
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid integer.")

            total = price * Decimal(quantity)
            tax = round(total * Decimal(0.05), 2)
            grand_total = total + tax

            cursor.execute("""
                INSERT INTO Sales (Customer_id, Product_id, quantity, sale_date)
                VALUES (?, ?, ?, ?);
                SELECT SCOPE_IDENTITY();
            """, (customer_id, product_id, quantity, datetime.now()))
            cursor.nextset()
            sale_id = cursor.fetchone()[0]

            cursor.execute("UPDATE Products SET quantity = quantity - ? WHERE Product_id = ?", (quantity, product_id))
            self.conn.commit()

            print(f"Sale recorded successfully. Total (incl. 5% tax): {grand_total}")
            Billing.generate_invoice(sale_id, customer_id, product_id, quantity, total, tax, grand_total)

        except Exception as e:
            print(f"Error creating sale: {e}")
      

    def daily_summary(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT CONVERT(date, sales.sale_date) AS SaleDate, SUM(products.price * sales.quantity) AS TotalSales
                FROM Sales
                JOIN Products ON sales.Product_id = products.Product_id
                GROUP BY CONVERT(date, sales.sale_date)
                ORDER BY CONVERT(date, sales.sale_date) DESC
            """)
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    print(f"Date: {row[0]}, Total Sales: {row[1]:.2f}")
            else:
                print("No sales records found for the selected period.")

        except Exception as e:
            print(f"Error fetching daily summary: {e}")

    
    def monthly_summary(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT YEAR(sale_date) AS SaleYear, MONTH(sale_date) AS SaleMonth, SUM(products.price * sales.quantity) AS TotalSales
                FROM Sales
                JOIN Products ON sales.product_id = products.product_id
                GROUP BY YEAR(sale_date), MONTH(sale_date)
                ORDER BY SaleYear DESC, SaleMonth DESC
            """)
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    print(f"Year: {row[0]}, Month: {row[1]}, Total Sales: {row[2]:.2f}")
            else:
                print("No sales records found for the selected period.")

        except Exception as e:
            print(f"Error fetching monthly summary: {e}")


    def export_sales_csv(self):
        try:
            data_folder = r"C:\Users\nimmakayala.charan\Desktop\inventory_sales\data"

            if not os.path.exists(data_folder):
                os.makedirs(data_folder)

            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Sales")
            rows = cursor.fetchall()

            file_path = os.path.join(data_folder, "sales.csv")

            with open(file_path, "w", newline='') as file:
                writer = csv.writer(file)
                writer.writerow([column[0] for column in cursor.description])
                writer.writerows(rows)
            print(f"Sales exported to {file_path}.")
        except Exception as e:
            print(f"Error exporting sales CSV: {e}")

    def alert_low_quantity(self, page=1, items_per_page=10):
        try:
            offset = (page - 1) * items_per_page
            cursor = self.conn.cursor()
            cursor.execute("""SELECT Product_id, Name, Category, Price, Quantity 
                           FROM products 
                           WHERE quantity < 5
                           ORDER BY Product_id
                           OFFSET ? ROWS FETCH NEXT ? ROWS ONLY
                           """, (offset, items_per_page))
            for product_id, name, category, price, quantity in cursor.fetchall():
                print(f"Low quantity alert: ({product_id}, '{name}', '{category}', ₹{format(price, '.2f')}, {quantity})")
        except Exception as e:
            print(f"Error checking low quantity: {e}")

    def view_sales(self,page=1, items_per_page=10):
        try:
            offset = (page - 1) * items_per_page 
            
            cursor = self.conn.cursor()
            cursor.execute("""
                           SELECT * FROM Sales
                           ORDER BY Sale_date DESC
                           OFFSET ? ROWS FETCH NEXT ? ROWS ONLY
                    """, (offset, items_per_page))
            sales = cursor.fetchall()
            if sales:
                for sale in sales:
                    print(sale)  
            else:
                print("No sales records found.")
        except Exception as e:
            print(f"Error viewing sales: {e}")

    def search_sales(self, keyword):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT * FROM Sales 
                WHERE Customer_id LIKE ? OR Product_id LIKE ?
            """, (f"%{keyword}%", f"%{keyword}%"))
            results = cursor.fetchall()
            if results:
                for row in results:
                    print(row)  
            else:
                print("No matching sales found.")
        except Exception as e:
            print(f"Error searching sales: {e}")

    
    def get_bill_details(self, sale_id):
        try:
            cursor = self.conn.cursor()

            if not isinstance(sale_id, int):
                print("sale_id must be an integer.")
                return

            cursor.execute("""
                SELECT 
                    s.Sale_id,
                    s.Sale_date,
                    c.Customer_id,
                    c.Name AS Customer_Name,
                    c.Phone AS Customer_Phone,
                    p.Product_id,
                    p.Name AS Product_name,
                    p.Price,
                    s.Quantity,
                    (p.Price * s.Quantity) AS Total,
                    ROUND(p.Price * s.Quantity * 0.05, 2) AS Tax,
                    ROUND(p.Price * s.Quantity * 1.05, 2) AS Grand_Total
                FROM Sales s
                JOIN Customers c ON s.Customer_id = c.Customer_id
                JOIN Products p ON s.Product_id = p.Product_id
                WHERE s.Sale_id = ?
            """, (sale_id,))

            result = cursor.fetchone()
            if not result:
                print("Sale not found.")
                return

            columns = [column[0] for column in cursor.description]
            sale_data = dict(zip(columns, result))

            print("\n" + "=" * 40)
            print(f"  Bill Details - Sale ID: {sale_data['Sale_id']}")
            print("=" * 40)

            print("\n --------Sale Info--------")
            print(f"  Sale Date        : {sale_data['Sale_date']}")

            print("\n --------Customer Info--------")
            print(f"  Customer ID      : {sale_data['Customer_id']}")
            print(f"  Name             : {sale_data['Customer_Name']}")
            print(f"  Phone            : {sale_data['Customer_Phone']}")

            print("\n --------Product Info--------")
            print(f"  Product ID       : {sale_data['Product_id']}")
            print(f"  Product Name     : {sale_data['Product_name']}")
            print(f"  Unit Price       : ${sale_data['Price']:.2f}")
            print(f"  Quantity         : {sale_data['Quantity']}")

            print("\n --------Billing--------")
            print(f"  Subtotal         : ${sale_data['Total']:.2f}")
            print(f"  Tax (5%)         : ${sale_data['Tax']:.2f}")
            print("=" * 40 + "\n")
            print(f"  Grand Total      : ${sale_data['Grand_Total']:.2f}")
            print("=" * 40 + "\n")
            

            return sale_data

        except Exception as e:
            print(f" Error retrieving sale: {e}")



   



            
    
