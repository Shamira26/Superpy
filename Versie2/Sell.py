from datetime import datetime
from HandleCsv import HandleCSV
import csv
import os

class sell:
    def __init__(self, handle_date_instance, csv_handler):
        self.handle_date = handle_date_instance
        self.csv_handler = csv_handler
        self.original_quantities = {}

     # Add this function to set the original quantity when buying a product.
    def set_original_quantity(self, product_name, quantity):
        self.original_quantities[product_name] = quantity    

    def check_stock(self, product_name, quantity, expiration_date):
        inventory_data = self.csv_handler.read()
        available_quantity = sum(
            int(row["Quantity"])
            for row in inventory_data
            if row["Product_name"] == product_name and row["Type"] == "Buy" and row["Expiration_date"] == expiration_date
        )

        if available_quantity < quantity:
            print(f"Error: Product '{product_name}' is not in stock.")
            return False

        return True
    

    def write(self, product_name, quantity, price):
        if not self.csv_handler:
            return

        data = self.csv_handler.read()

     # Find "buy" products with the same name as the sold product and sort them by expiration date
        matching_buys = [row for row in data 
                         if row["Type"] == "Buy" 
                         and row["Product_name"] == product_name 
                         and row.get("Status") != "Not active"
                         ]
        matching_buys = sorted(matching_buys, key=lambda x: datetime.strptime(x["Expiration_date"], "%Y-%m-%d"))

        if not matching_buys:
            print(f"Error: No inventory found for '{product_name}'.")
            return

        current_date = self.handle_date.read()

        self.set_original_quantity(product_name, quantity)

        # Filter "buy" products with a future expiration date
        future_expirations = [buy for buy in matching_buys if datetime.strptime(buy["Expiration_date"], "%Y-%m-%d") >= current_date]

        if not future_expirations:
            print(f"Error: All available products for '{product_name}' have expired.")
            return

        # Check if there is enough stock to sell
        remaining_quantity = quantity
        for buy in future_expirations:
            if remaining_quantity <= 0:
                break

            buy_quantity = int(buy["Quantity"])
            if buy_quantity >= remaining_quantity:
                # The "buy" has enough stock to cover the remaining quantity
                buy["Quantity"] = str(buy_quantity - remaining_quantity)
                self.set_original_quantity(product_name, buy_quantity)  # Save the original quantity
                remaining_quantity = 0
            else:
                # The "buy" doesn't have enough stock, so sell what is available and move on to the next
                remaining_quantity -= buy_quantity
                self.set_original_quantity(product_name, buy_quantity) 
                buy["Quantity"] = "0"


        if remaining_quantity > 0:
            print("Error: Selling more than the available quantity is not possible.")
            return

        # Add a new "sell" record
        data_row = {
            "Type": "Sell",
            "Product_name": product_name,
            "Quantity": quantity,
            "Price": price,
            "Date": current_date.strftime("%Y-%m-%d"),
            "Expiration_date": future_expirations[0]["Expiration_date"]
        }
        data.append(data_row) # Add the new "sell" record to the list

        # Update the CSV with the modified "buy" records
        for buy in future_expirations:
            if int(buy["Quantity"]) <= 0:
        # Update the status of "buy" records with a quantity of 0 to "SOLD"
                buy["Status"] = "Sold"
            else:
                buy["Quantity"] = str(max(0, int(buy["Quantity"]) - remaining_quantity))


        self.csv_handler.write_all(data)  # Write all records to the CSV
        print(f"Sale recorded for product '{product_name}'.")

    def complete_sell(self, product_name, quantity, price):
        data = self.csv_handler.read()
        current_date = self.handle_date.read()

        matching_buys = [row for row in data
                        if row["Type"] == "Buy"
                        and row["Product_name"] == product_name
                        and row["Status"] == "Active"
                        ]
        matching_buys = sorted(matching_buys, key=lambda x: datetime.strptime(x["Expiration_date"], "%Y-%m-%d"))

        if not matching_buys:
            print(f"Error: No matching 'Buy' records found for '{product_name}'.")
            return

        total_available_quantity = sum(int(buy["Quantity"]) for buy in matching_buys)

        if total_available_quantity < quantity:
            print(f"Error: Selling more than the available quantity is not possible.")
            return

        remaining_quantity = quantity

        for buy in matching_buys:
            available_quantity = int(buy["Quantity"])

            if available_quantity >= remaining_quantity:
                expiration_date = buy["Expiration_date"]

                if available_quantity == remaining_quantity:
                    buy["Status"] = "Sold"
                    self.set_original_quantity(product_name, available_quantity)
                    buy["Quantity"] = str(available_quantity)
                    print(f"Sold record updated: Quantity set to {buy['Quantity']}")

                else:
                    buy["Quantity"] = str(available_quantity - remaining_quantity)
                    print(f"Sold record updated: Quantity set to {buy['Quantity']}")

                data_row = {
                    "Type": "Sell",
                    "Product_name": product_name,
                    "Quantity": remaining_quantity,
                    "Price": price,
                    "Date": current_date.strftime("%Y-%m-%d"),
                    "Expiration_date": expiration_date
                }
                data.append(data_row)
                self.csv_handler.write_all(data)
                print(f"Sale recorded for product '{product_name}'.")
                return
            
            else:
                print("Sold record updated: Status set to 'Sold'")
                buy["Quantity"] = "0"
                if buy["Status"] == "Active":
                    original_quantity = self.original_quantities.get(product_name)
                    print(f"Sold record updated: Quantity set to  {original_quantity}")
                    buy["Quantity"] = str(original_quantity)
                    buy["Status"] = "Sold"

            #else:
             #   buy["Quantity"] = "0"
              #  if buy["Status"] == "Active":
               #     buy["Status"] = "Sold"
              #      print(f"Sold record updated: Status set to 'Sold'")
#
                    data_row = {
                        "Type": "Sell",
                        "Product_name": product_name,
                        "Quantity": available_quantity,
                        "Price": price,
                        "Date": current_date.strftime("%Y-%m-%d"),
                        "Expiration_date": buy["Expiration_date"]
                    }
                    data.append(data_row)
                    remaining_quantity -= available_quantity

            print(f"Sale recorded for product '{product_name}'.")
