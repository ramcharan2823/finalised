import csv
import os
import re
from db_config import database_connection

class Product:
    def __init__(self):
        self.conn = database_connection()
        print("Connected to database")

    def is_valid_name(self, name):
        pattern = r'^[A-Za-z\s]+$'
        if isinstance(name, str) and name.strip() != "":
            return bool(re.match(pattern, name.strip()))
        return False

    def is_product_exists(self, product_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM Products WHERE Product_id = ?", (product_id,))
            result = cursor.fetchone()[0]
            return result > 0 
        except Exception as e:
            print(f"Error checking product existence: {e}")
            return False

    def generate_product_id(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT MAX(product_id) FROM Products")
            result = cursor.fetchone()
            if result[0] is None:
                next_id = 1
            else:
                max_id = int(result[0][4:])
                next_id = max_id + 1
            return f"PROD{next_id:04}"
        except Exception as e:
            print(f"Error generating product ID: {e}")
            return None

    def add_product(self):
        try:
            while True:
                name = input("Product name: ").strip()
                if not self.is_valid_name(name):
                    print("Name must be a non-empty string with only letters and spaces.")
                else:
                    break
            while True:
                category = input("Category: ").strip()
                if not self.is_valid_name(category):
                    print("Category must be a non-empty string with only letters and spaces.")
                else:
                    break
            while True:
                price_input = input("Price: ").strip()
                try:
                    price = float(price_input)
                    if price <= 0:
                        print("Price must be a positive number.")
                    else:
                        break
                except ValueError:
                    print("Invalid input. Please enter a decimal number.")
            while True:
                quantity_input = input("Stock quantity: ").strip()
                try:
                    quantity = int(quantity_input)
                    if quantity < 0:
                        print("Quantity must be a non-negative integer.")
                    else:
                        break
                except ValueError:
                    print("Invalid input. Please enter an integer.")
                    
            product_id = self.generate_product_id()
            if product_id is None:
                print("Could not generate product ID.")
                return

            cursor = self.conn.cursor()
            cursor.execute("""
                INSERT INTO Products (Product_id, Name, Category, Price, Quantity)
                VALUES (?, ?, ?, ?, ?)
            """, (product_id, name, category, price, quantity))
            self.conn.commit()
            print(f"Product '{name}' added successfully with ID {product_id}.")

        except Exception as e:
            print(f"Error adding product: {e}")


    def update_product_details(self):
        try:
            product_id = input("Product ID to update: ").strip()

            cursor = self.conn.cursor()
            cursor.execute("SELECT Name, Category, Price, Quantity FROM Products WHERE Product_id=?", (product_id,))
            result = cursor.fetchone()

            if not result:
                print("Product not found.")
                return

            current_name, current_category, current_price, current_quantity = result

            while True:
                name = input("New name (leave blank to keep unchanged): ").strip()
                if name == "":
                    new_name = current_name
                    break
                elif not self.is_valid_name(name):
                    print("Name must contain only letters and spaces. Please try again.")
                else:
                    new_name = name
                    break

            while True:
                category = input("New category (leave blank to keep unchanged): ").strip()
                if category == "":
                    new_category = current_category
                    break
                elif not self.is_valid_name(category):
                    print("Category must contain only letters and spaces. Please try again.")
                else:
                    new_category = category
                    break

            while True:
                price_input = input("New price (leave blank to keep unchanged): ").strip()
                if price_input == "":
                    new_price = current_price
                    break
                try:
                    price_val = float(price_input)
                    if price_val <= 0:
                        print("Price must be a positive number. Please try again.")
                    else:
                        new_price = price_val
                        break
                except ValueError:
                    print("Invalid input. Please enter a decimal number.")

            while True:
                quantity_input = input("New quantity (leave blank to keep unchanged): ").strip()
                if quantity_input == "":
                    new_quantity = current_quantity
                    break
                try:
                    qty_val = int(quantity_input)
                    if qty_val < 0:
                        print("Quantity must be a non-negative integer. Please try again.")
                    else:
                        new_quantity = qty_val
                        break
                except ValueError:
                    print("Invalid input. Please enter an integer number.")

            cursor.execute("""
                UPDATE Products
                SET Name = ?, Category = ?, Price = ?, Quantity = ?
                WHERE Product_id = ?
            """, (new_name, new_category, new_price, new_quantity, product_id))
            self.conn.commit()
            print("Product updated successfully.")

        except Exception as e:
            print(f"Error updating product: {e}")


    def view_products(self, page=1, page_size=10):
        try:
            cursor = self.conn.cursor()
            offset = (page - 1) * page_size
            cursor.execute("SELECT * FROM Products ORDER BY product_id OFFSET ? ROWS FETCH NEXT ? ROWS ONLY", (offset, page_size))
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    print(row)
            else:
                print("No products on this page.")
        except Exception as e:
            print(f"Error viewing products: {e}")

    def delete_product(self, product_id):
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM Products WHERE product_id=?", (product_id,))
            self.conn.commit()
            print(f"Product {product_id} deleted successfully.")
        except Exception as e:
            print(f"Error deleting product: {e}")

    def search_product(self, keyword):
        try:
            cursor = self.conn.cursor()
            cursor.execute("""
                SELECT * FROM Products
                WHERE Name LIKE ? OR category LIKE ?
            """, (f"%{keyword}%", f"%{keyword}%"))
            results = cursor.fetchall()
            if results:
                for row in results:
                    print(row)
            else:
                print("No matching products found.")
        except Exception as e:
            print(f"Error searching product: {e}")

    def export_products_csv(self):
        try:
            data_folder = r"C:\Users\nimmakayala.charan\Desktop\inventory_sales\data"

            if not os.path.exists(data_folder):
                os.makedirs(data_folder)

            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM Products")
            rows = cursor.fetchall()

            file_path = os.path.join(data_folder, "products.csv")

            with open(file_path, "w", newline='') as file:
                writer = csv.writer(file)
                writer.writerow([column[0] for column in cursor.description])
                writer.writerows(rows)
            print(f"Products exported to {file_path}.")
        except Exception as e:
            print(f"Error exporting products CSV: {e}")

    def import_products_csv(self, filename):
        try:
            data_folder = r"C:\Users\nimmakayala.charan\Desktop\inventory_sales\data"

            if not os.path.exists(data_folder):
                os.makedirs(data_folder)

            file_path = os.path.join(data_folder, filename)

            cursor = self.conn.cursor()
            with open(file_path, newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    cursor.execute("""
                        INSERT INTO Products (product_id, Name, category, quantity, price)
                        VALUES (?, ?, ?, ?, ?)
                    """, (row['product_id'], row['Name'], row['category'], int(row['quantity']), float(row['price'])))
            self.conn.commit()
            print(f"Products imported from {file_path}.")
        except Exception as e:
            print(f"Error importing products from CSV: {e}")


    

