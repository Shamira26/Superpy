from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from rich.console import Console
from rich.table import Table

class report:

    def __init__(self, handle_date_instance, csv_handler):
        self.handle_date = handle_date_instance
        self.csv_handler = csv_handler
        self.data = self.read()

    def read(self):
        # Read all rows from the CSV file and store the data
        return self.csv_handler.read()

    def print_data(self):
        for row in self.data:
            print(row)

    def inventory(self, start_date=None, end_date=None, inventory_type=None):
        data = self.csv_handler.read()
        
        # Filter transactions based on inventory type
        if inventory_type == "buy":
            transactions = [row for row in data if row["Type"] == "Buy"]
        elif inventory_type == "sell":
            transactions = [row for row in data if row["Type"] == "Sell"]
        else:
            transactions = data

        # Filter transactions based on start and end dates
        if start_date and end_date:
            transactions = [row for row in transactions if start_date <= datetime.strptime(row["Date"], "%Y-%m-%d") <= end_date]

        console = Console()

        if not transactions:
            console.print(f"No {inventory_type} inventory.")
        else:
            # Display the inventory data in a table using the rich library
            table = Table(show_header=True )
            table.add_column("Product", style="dim", width=17)
            table.add_column("Quantity", justify="left", width=9)
            table.add_column("Price", justify="left", width=10)
            table.add_column("Date", justify="left", width=11)
            table.add_column("Expiration_date", justify="left", width=15)

            for row in transactions:
                table.add_row(row['Product_name'], str(row['Quantity']), str(row['Price']), row['Date'], row['Expiration_date'])

            console.print(table)

    def get_revenue(self, date = None):
        data = self.csv_handler.read()

        if not date:
            date = self.handle_date.read().strftime("%Y-%m-%d")

        actions_on_date = [row for row in data if row["Date"] == date and row["Type"] == "Sell"]
        # Calculate total revenue
        revenue = sum((float(row["Quantity"])*float(row["Price"])) for row in actions_on_date)
        return revenue
    
    def get_cost(self, date = None):
        data = self.csv_handler.read()

        if not date:
            date = self.handle_date.read().strftime("%Y-%m-%d")
        
        
        actions_on_date = [row for row in data if row["Date"] == date and row["Type"] == "Buy"]
        total_cost = sum((float(row["Quantity"])*float(row["Price"])) for row in actions_on_date)
        return total_cost
    
    def revenue(self, start_date=None, end_date=None):
        total_revenue = self.get_revenue(start_date=start_date, end_date=end_date)
        print(f"Total Revenue is {round(total_revenue, 2)}")

    def profit(self, date = None):
        revenue = self.get_revenue(date=date)
        total_cost = self.get_cost(date=date)
        profit = revenue - total_cost
        print(f"Total Profit is {round(profit, 2)}" )
        
    def plot_profit(self, start_date, end_date):
        data = self.csv_handler.read()
       
        # Generate a date range for plotting profit
        date_range = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]
        # Get profit data for each date in the range.
        profit_data = [self.get_profit(date=date.strftime("%Y-%m-%d")) for date in date_range]

        # Plot profit data using matplotlib.
        plt.ion()  
        fig, ax = plt.subplots()
    
        ax.plot(date_range, profit_data, color='#bfae7e', linestyle='-', linewidth=2, marker='o', markersize=4)
        ax.set_xlabel('Date',fontfamily='sans-serif', fontname='Verdana', fontsize=12, fontweight='normal', color='#bfae7e')
        ax.set_ylabel('Profit',fontfamily='sans-serif', fontname='Verdana', fontsize=12, fontweight='normal', color='#bfae7e')
        ax.set_title('Profit Over Time',fontfamily='sans-serif', fontname='Verdana', fontsize=14, fontweight='normal', color='#bfae7e')
        ax.set_facecolor('#f5f3eb') 
        plt.show()
               
        # Prevent the script from closing until the user presses Enter
        input("Press Enter to continue...")

    def get_profit(self, date=None):
        data = self.csv_handler.read()

        if not date:
            date = self.handle_date.read().strftime("%Y-%m-%d")

        actions_on_date = [row for row in data if row["Date"] == date]
        # Calculate revenue for "Sell" actions on the date.
        revenue = sum(float(row["Quantity"]) * float(row["Price"]) for row in actions_on_date if row["Type"] == "Sell")
        # Calculate cost for "Buy" actions on the date.
        total_cost = sum(float(row["Quantity"]) * float(row["Price"]) for row in actions_on_date if row["Type"] == "Buy")
        # Calculate profit
        profit = revenue - total_cost

        return round(profit, 2)    

