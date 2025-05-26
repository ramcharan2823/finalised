import os
from datetime import datetime

class Billing:
    @staticmethod
    def generate_invoice(sale_id,customer_id, product_id, quantity, total, tax, grand_total):
        try:
            data_folder = r"C:\Users\nimmakayala.charan\Desktop\inventory_sales\reports\invoices"
            if not os.path.exists(data_folder):
                os.makedirs(data_folder)

            filename = f"invoice__{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"
            file_path = os.path.join(data_folder, filename)

            with open(file_path, "w",encoding="utf-8") as file:
                file.write("="*50 + "\n")
                file.write("{:^50}\n".format("INVENTORY STORE"))
                file.write("{:^50}\n".format("Invoice"))
                file.write("="*50 + "\n")
                file.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                file.write("-"*50 + "\n")
                file.write(f"Sale ID: {sale_id}\n")
                file.write(f"Customer ID : {customer_id}\n")
                file.write(f"Product ID  : {product_id}\n")
                file.write(f"Quantity    : {quantity}\n")
                file.write("-"*50 + "\n")
                file.write(f"{'Subtotal':<20}: ₹{total:,.2f}\n")
                file.write(f"{'Tax (5%)':<20}: ₹{tax:,.2f}\n")
                file.write(f"{'Grand Total':<20}: ₹{grand_total:,.2f}\n")
                file.write("="*50 + "\n")
                file.write("{:^50}\n".format("Thank you for shopping with us!"))
                file.write("="*50 + "\n")

            print(f"Invoice generated and saved to:\n{file_path}")
        except Exception as e:
            print(f"Error generating invoice: {e}")

    






