from datetime import datetime, timedelta
from HandleCsv import HandleCSV

class HandleDate: 

    def __init__ (self):
        self.today = self.read()

    def advanced(self, amount):
        # Advance the current date by the specified number of days
        self.today = self.today + timedelta(days= amount)
        self.write(self.today)
        print(f"The current date is now: {self.today.strftime('%Y-%m-%d')}")

    def write(self, dt):
        # Write the given date to the file in the specified format
        with open("Today.txt", "w") as file:
            file.write(dt.strftime("%Y-%m-%d"))

    def read(self) -> datetime:
        with open("Today.txt","r") as file:
            dt = file.read()
            # If the file is empty, write the current date and read it again
            dt = dt.strip()
            if dt != '':
                return datetime.strptime(dt, "%Y-%m-%d")
            self.write(datetime.now())
            return self.read()
        
    def set(self, date):
        """
        Set the current date to the specified date and update the 'today.txt' file.

        Args:
            date (datetime): The new date to set in 'YYYY-MM-DD' format.

        Returns:
            None
        """
        with open("Today.txt", "w") as file:
            file.write(date.strftime("%Y-%m-%d"))
        self.today = date    
