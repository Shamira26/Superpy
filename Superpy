import argparse
import csv 
import os
import matplotlib.pyplot as plt 
from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table
from Report import report
from Buy import buy
from Sell import sell 
from DateHandler import HandleDate

class HandleCSV:

    def __init__(self, filename):
        self.filename = filename

        # If the specified file doesn't exist, create a new CSV file with the correct headers
        if not os.path.exists(filename):
            with open(filename, "w", newline='') as csvfile:
                fieldnames = ["Type","Product_name", "Quantity", "Price", "Date", "Expiration_date"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()    


    def write(self, row):
         # Append a row to the CSV file.
        with open(self.filename, "a", newline='') as csvfile: 
            fieldnames = ["Type","Product_name", "Quantity", "Price", "Date", "Expiration_date"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write the new row
            writer.writerow(row)

    def write_all(self, data):
        with open(self.filename, "w", newline='') as csvfile:
            fieldnames = ["Type","Product_name", "Quantity", "Price", "Date", "Expiration_date"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write the header
            writer.writeheader()

            # Write all rows
            for row in data:
                writer.writerow(row)
                
    def read(self):
        # Read all rows from the CSV file and return them as a list of dictionaries
        with open(self.filename, "r", newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            data = [row for row in reader]
        return data  
        
    
if __name__ == "__main__":

    today = HandleDate()
    csv_handler = HandleCSV("Transaction_data.csv")
    buy_instance = buy(today, csv_handler)
    sell_instance = sell(today,csv_handler)
    report_instance = report(today, csv_handler)

    console = Console()

    parser = argparse.ArgumentParser(
                    prog="SuperPy",
                    description="A script to keep track of purchase, sale, and reporting of products"
                    )
    
    parser.add_argument("Options", nargs="*", type=str, help="Specify the operation (buy, sell, report) and additional arguments.")
    parser.add_argument("--advanced-time", type=int, help="Advance the current date by a specified number of days.")
    parser.add_argument("--product_name", type=str, help="Specify the product name.", required=False)
    parser.add_argument("--quantity", type=int, help="Specify the quantity of the product.", required=False)
    parser.add_argument("--price", type=float, help="Specify the price of the product.", required=False)
    parser.add_argument("--expiration_date", type=str, help="Specify the expiration date of the product.Format: YYYY-MM-DD", required=False)
    parser.add_argument("--date", type=str, help="Specify a date for reporting purposes.", default=None)
   # parser.add_argument("--inventory", action="store_true", help="List all products in inventory")
    parser.add_argument("--inventory-type", type=str, choices=["buy", "sell"], help="Specify the type of inventory to display (buy, sell)")

    parser.add_argument("--plot-profit", action="store_true", default=False, help="Plot profit over time")
    parser.add_argument("--start-date", type=str, help="Specify a start date for reporting purposes. Format: YYYY-MM-DD ")
    parser.add_argument("--end-date", type=str, help="Specify a end date for reporting purposes. Format: YYYY-MM-DD")
 
    args=parser.parse_args()

    if len(args.Options) == 0 :
        if args.advanced_time:
            today.advanced(args.advanced_time)
    else:
        if args.Options[0] == "buy":
            outcome = buy(today, csv_handler)
            outcome.write(args.product_name, args.quantity, args.price, args.expiration_date)

        elif args.Options[0] == "sell":
            outcome = sell(today, csv_handler)
            outcome.write(args.product_name, args.quantity, args.price, args.expiration_date)

        elif args.Options[0] == "report":
            outcome = report_instance
            outcome.read()

            if args.Options[1] == "revenue":
                outcome.revenue(args.start_date, args.end_date)

            elif args.Options[1] == "inventory":
                start_date = datetime.strptime(args.start_date, "%Y-%m-%d") if args.start_date else None
                end_date = datetime.strptime(args.end_date, "%Y-%m-%d") if args.end_date else None

                outcome.inventory(start_date, end_date, args.inventory_type)            

            elif args.Options[1] == "profit":
                outcome.profit(args.date)  
                if args.plot_profit:
                    start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
                    end_date = datetime.strptime(args.end_date, "%Y-%m-%d")
        
                    outcome.plot_profit(start_date, end_date)
             
    #print(today.today)

