from datetime import datetime, timedelta
import csv
import os

class sell:
    def __init__(self, handle_date_instance, csv_handler):
        self.handle_date = handle_date_instance
        self.csv_handler = csv_handler

    def check_stock(self, product_name, quantity):
        # Check if the given product has enough quantity in stock
        inventory_data = self.csv_handler.read()
        available_quantity = sum(
            int(row["Quantity"]) for row in inventory_data if row["Product_name"] == product_name
        )

        return available_quantity >= quantity
       
    def write(self, product_name, quantity, price, expiration_date):
        # Check if the expiration date is in the future
        if datetime.strptime(expiration_date, "%Y-%m-%d") < datetime.now():
            print("Warning: The expiration date is in the past. Sale not recorded.")
            return

        # Check if the product is in stock
        if not self.check_stock(product_name, quantity):
            print(f"Error: Product '{product_name}' is not in stock or there is not enough quantity.")
            return  
          
        data_row = {
            "Type": "Sell",
            "Product_name": product_name,
            "Quantity": quantity,
            "Price": price,
            "Date": self.handle_date.read().strftime("%Y-%m-%d"),
            "Expiration_date": expiration_date
        }
        self.csv_handler.write(data_row)
        print(f"Sale recorded for product '{product_name}'.")
