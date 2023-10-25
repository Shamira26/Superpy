import os
import csv

class HandleCSV:

    def __init__(self, filename):
        self.filename = filename

        # If the specified file doesn't exist, create a new CSV file with the correct headers
        if not os.path.exists(filename):
            with open(filename, "w", newline='') as csvfile:
                fieldnames = ["Type","Product_name", "Quantity","Original_quantity","Price", "Date", "Expiration_date","Status"]
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()    


    def write(self, row):
         # Append a row to the CSV file.
        with open(self.filename, "a", newline='') as csvfile: 
            fieldnames = ["Type","Product_name", "Quantity","Original_quantity","Price", "Date", "Expiration_date","Status"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            # Write the new row
            writer.writerow(row)

    def write_all(self, data):
        with open(self.filename, "w", newline='') as csvfile:
            fieldnames = ["Type","Product_name", "Quantity", "Original_quantity", "Price", "Date", "Expiration_date","Status"]
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
        
