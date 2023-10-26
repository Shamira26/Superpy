from datetime import datetime
from HandleCsv import HandleCSV
import csv
import os

class buy:
    def __init__(self, handle_date_instance, csv_handler):
        self.handle_date = handle_date_instance
        self.csv_handler = csv_handler
        self.product_history = []
        self.original_quantities = {}  

    def write(self, product_name, quantity, price, expiration_date):
        data = self.csv_handler.read()
        current_date = self.handle_date.read()

        if datetime.strptime(expiration_date, "%Y-%m-%d") < current_date:
            print("Error: Expiration date is in the past. Product cannot be bought.")
            return    

        # Check if there is an existing record with the same details
        for row in data:
            if (
                row["Type"] == "Buy"
                and row["Product_name"] == product_name
                and float(row["Price"]) == price
                and row["Expiration_date"] == expiration_date
            ):
                if quantity is not None:
                    # Update quantity if the details match
                    row["Quantity"] = str(int(row["Quantity"]) + quantity)
                    self.original_quantities[product_name] = int(row["Original_quantity"]) 
                    self.csv_handler.write_all(data)
                    print(f"Quantity updated for existing product '{product_name}'.")
                else:
                    print("Error: Quantity is not provided.")
                return

        # If no existing record is found, create a new one
        data_row = {
            "Type": "Buy",
            "Product_name": product_name,
            "Quantity": quantity,
            "Original_quantity": quantity,  
            "Price": price,
            "Date": current_date.strftime("%Y-%m-%d"),
            "Expiration_date": expiration_date,
            "Status": "Active"  
        }
        # Keep track of the original quantity
        self.original_quantities[product_name] = quantity  
        self.csv_handler.write(data_row)
        print(f"OK! Product is added successfully.")

    def update_status(self):
        data = self.csv_handler.read()
        current_date = self.handle_date.read()

        for row in data:
            if row["Type"] == "Buy" and row.get("Status") != "Not active":
                expiration_date = datetime.strptime(row["Expiration_date"], "%Y-%m-%d")
                if expiration_date < current_date:
                    row["Status"] = "Not active"

        self.csv_handler.write_all(data)

    def update_product_status(self, product_name):
        data = self.csv_handler.read()

        for row in data:
            if row["Type"] == "Buy" and row["Product_name"] == product_name:
                if int(row["Quantity"]) == 0:
                    row["Status"] = "Sold"

        self.csv_handler.write_all(data)

    def complete_sell(self, product_name, quantity, price):
        data = self.csv_handler.read()
        self.mark_as_sold(product_name)

        for row in data:
            if row["Type"] == "Buy" and row["Product_name"] == product_name and row["Status"] != "Not active":
                if int(row["Quantity"]) - quantity <= 0:
                    print(f"Changing status for product: {row['Product_name']} to Sold out")
                    row["Status"] = "Sold"
                    row["Quantity"] = "0"
                else:
                    # Here you call the buy class and pass the values
                    outcome = buy(self.handle_date, self.csv_handler)
                    outcome.complete_buy(product_name, quantity, row["Expiration_date"])
                    row["Quantity"] = str(int(row["Quantity"]) - quantity)

                # Update the original quantities if the product is in self.original_quantities
                if product_name in self.original_quantities:
                    self.original_quantities[product_name] -= quantity

        self.csv_handler.write_all(data)

    def add_to_product_history(self, product_name, quantity, price, date):
        # First, look for the item in product_history
        found = False
        for item in self.product_history:
            if item["Product_name"] == product_name:
                item["Quantity"] += quantity
                found = True
                break

        # If the item is not found in product_history, add a new item
        if not found:
            item = {
                "Product_name": product_name,
                "Quantity": quantity,
                "Price": price,
                "Date": date,
                "Status": "Active"  
            }
            self.product_history.append(item)

        # Update item statuses to "Sold" when the quantity is 0
        for item in self.product_history:
            if item["Quantity"] == 0:
                item["Status"] = "Sold"

    def mark_as_sold(self, product_name, expiration_date):
        for item in self.product_history:
            if item["Product_name"] == product_name and item["Quantity"] == 0:
                item["Status"] = "Sold"
                item["Expiration_date"] = expiration_date
