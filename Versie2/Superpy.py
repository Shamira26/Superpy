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
from HandleCsv import HandleCSV
from DateHandler import HandleDate

def main():
    today = HandleDate()
    csv_handler = HandleCSV("Transaction_data12.csv")
    buy_instance = buy(today, csv_handler)
    sell_instance = sell(today, csv_handler) 
    report_instance = report(today, csv_handler, buy_instance)

    console = Console()

    parser = argparse.ArgumentParser(
                    prog="SuperPy",
                    description="An inventory tool to keep track of purchase, sale and reporting of products"
                    )
    
    subparsers = parser.add_subparsers(title="subcommands",dest="subcommand", description="valid subcommands", help="additional help")


    # Subparser for the 'buy' subcommand
    buy_parser = subparsers.add_parser("buy", help="Record a purchase")
    buy_parser.add_argument("--product_name", type=str, help="Specify the product name.", required=True)
    buy_parser.add_argument("--quantity", type=int, help="Specify the quantity of the product.", required=True)
    buy_parser.add_argument("--price", type=float, help="Specify the price of the product.", required=True)
    buy_parser.add_argument("--expiration_date", type=str, help="Specify the expiration date of the product.", required=True)

    # Subparser for the 'sell' subcommand
    sell_parser = subparsers.add_parser("sell", help="Sell a purchase")
    sell_parser.add_argument("--product_name", type=str, help="Specify the product name.", required=True)
    sell_parser.add_argument("--quantity", type=int, help="Specify the quantity of the product.", required=True)
    sell_parser.add_argument("--price", type=float, help="Specify the price of the product.", required=True)

    # Subparser for the 'report' subcommand
    report_parser = subparsers.add_parser("report", help="Report offers insights into your inventory, revenue, and profit")
    report_subparsers = report_parser.add_subparsers(title="subcommands",dest="report_subcommand",description="valid subcommands", help="additional help")

    # Subparser for the 'inventory' subcommand
    inventory_parser = report_subparsers.add_parser("inventory", help="Inventory report for ??? records")
    inventory_parser.add_argument("--inventory-type", type=str, choices=["buy", "sell"], help="Specify the type of inventory to display (buy, sell)")
    inventory_parser.add_argument("--start-date", type=str, help="Specify a start date for reporting purposes. Format: YYYY-MM-DD")
    inventory_parser.add_argument("--end-date", type=str, help="Specify an end date for reporting purposes. Format: YYYY-MM-DD")

    # Subparser for the 'revenue' subcommand
    revenue_parser = report_subparsers.add_parser("revenue", help="Revenue report")
    revenue_parser.add_argument("--date", type=str, help="Specify a date for reporting purposes. Format: YYYY-MM-DD")

    # Subparser for the 'profit' subcommand
    profit_parser = report_subparsers.add_parser("profit", help="Profit report")
    profit_parser.add_argument("--date", type=str, help="Specify a date for reporting purposes. Format: YYYY-MM-DD")
    profit_parser.add_argument("--plot-profit", action="store_true", default=False, help="Plot profit over time")
    profit_parser.add_argument("--start-date", type=str, help="Specify a start date for profit purposes. Format: YYYY-MM-DD")
    profit_parser.add_argument("--end-date", type=str, help="Specify an end date for profit puoses. Format: YYYY-MM-DD")

    # Days
    parser.add_argument("--advanced-time", type=int, help="Advance the current date by a specified number of days.")
    parser.add_argument("--set-date", type=str, help="Set the current date to the specified date (YYYY-MM-DD)")
    
    args=parser.parse_args()

    if args.advanced_time:
        today.advanced(args.advanced_time)
        buy_instance.update_status()  # Werk de "Status" bij voor buy-records
   
    if args.set_date:
        try:
            set_date = datetime.strptime(args.set_date, "%Y-%m-%d")
            today.set(set_date)
            print(f"Date set to {set_date.strftime('%Y-%m-%d')}")
            buy_instance.update_status()  # Werk de "Status" bij voor buy-records
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD format.")
        

    if args.subcommand == "buy":
        # Handle the 'buy' subcommand and its specific arguments
        print("Executing 'buy' subcommand")
        print(f"Product Name: {args.product_name}")
        print(f"Quantity: {args.quantity}")
        print(f"Price: {args.price}")
        print(f"Expiration Date: {args.expiration_date}")
        outcome = buy(today, csv_handler)
        outcome.write(args.product_name, args.quantity, args.price, args.expiration_date)

    elif args.subcommand == "sell":
        # Handle the sell subcommand and its specific arguments
        print("Executing 'sell' subcommand")
        print(f"Product Name: {args.product_name}")
        print(f"Quantity: {args.quantity}")
        print(f"Price: {args.price}")
        outcome = sell(today, csv_handler)
        outcome.complete_sell(args.product_name, args.quantity, args.price) 
        #outcome.write(args.product_name, args.quantity, args.price)

    elif args.subcommand == "report":
        if args.report_subcommand == "inventory":
            start_date = datetime.strptime(args.start_date, "%Y-%m-%d") if args.start_date else None
            end_date = datetime.strptime(args.end_date, "%Y-%m-%d") if args.end_date else None
            report_instance.inventory(start_date, end_date, args.inventory_type)
        elif args.report_subcommand == "revenue":
            outcome = report_instance
            outcome.revenue(args.date)
        elif args.report_subcommand == "profit":
            outcome = report_instance
            if args.date:
                date = datetime.strptime(args.date, "%Y-%m-%d")
                outcome.profit(date)
            else:
                start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
                end_date = datetime.strptime(args.end_date, "%Y-%m-%d")
                outcome.plot_profit(start_date, end_date)

if __name__ == "__main__":
    main()

