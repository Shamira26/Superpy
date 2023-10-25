from datetime import datetime, timedelta

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
            if dt != '':
                return datetime.strptime(dt, "%Y-%m-%d")
            self.write(datetime.now())
            return self.read()
