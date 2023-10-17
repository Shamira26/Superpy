from datetime import datetime
import csv
import os

class buy:
    def __init__(self, handle_date_instance, csv_handler):
        self.handle_date = handle_date_instance
        self.csv_handler = csv_handler

    def write(self, product_name, quantity, price, expiration_date):
        data = self.csv_handler.read()

        # Check if all the required arguments are provided; otherwise, provide a message
        if not (product_name and quantity and price and expiration_date):
            print("Error: All required arguments (product_name, quantity, price, expiration_date) must be provided.")
            return    

        # Check if there is an existing record with the same details 
        for row in data:
            if (
                row["Type"] == "Buy"
                and row["Product_name"] == product_name
                and float(row["Price"]) == price
                and row["Expiration_date"] == expiration_date
            ):
                # Update quantity if the details match
                row["Quantity"] = str(int(row["Quantity"]) + quantity)
                self.csv_handler.write_all(data)
                print(f"Quantity updated for existing product '{product_name}'.")
                return

        # If no existing record is found, create a new one
        data_row = {
            "Type": "Buy",
            "Product_name": product_name,
            "Quantity": quantity,
            "Price": price,
            "Date": self.handle_date.read().strftime("%Y-%m-%d"),
            "Expiration_date": expiration_date
        }
        self.csv_handler.write(data_row)
        print(f"OK! Product is added successfully.")


