# UsageGuide

This guide provides detailed information on using the SuperPy application, including a breakdown of available commands, options, and examples to help navigate.

## Advance Time
The `--advanced-time` option allows you to advance the current date in the SuperPy application by a specified number of days. This can be useful for simulating actions on different dates without waiting for the actual passage of time. 

#### Usage
```python
python superpy.py --advanced-time <number_of_days> 
```

Replace <number_of_days> with the desired number of days to advance the current date.

#### Example
To advance the current date by 6 days:

```python
python superpy.py --advanced-time 6
```

Notes:
- The --advanced-time command allows you to simulate time passing in the system. It doesn't affect the actual system time.
- If you use a negative value for the days, you can also adjust the date to the past.
- The current date is displayed after the time advancement.


## Set Date
The `--set-date` option enables you to set the current date to a specified date in the SuperPy application. This feature is helpful when you want to work with specific dates without waiting for real-time progression.

#### Usage

```python
python superpy.py --set-date <date in YYYY-MM-DD format>
```

#### Example
To set the current date to Christmas Eve:

```python
python superpy.py --set-date 2023-12-24
```

Notes:
- After setting the date, the new current date is displayed in the terminal and written to the today.txt file.



## Buy
The buy command allows you to record the purchase of products in your inventory. 

- --product_name: Specify the name of the product you're buying.
- --quantity: Specify the quantity of the product you're buying.
- --price: Specify the price per unit of the product.
- --expiration_date: Specify the expiration date of the product.

#### Usage
```python
python superpy.py buy --product_name <your product name> --quantity <your quantity> --price <your price> --expiration_date <your expiration date in YYYY-MM-DD format>
```

#### Example
This will record a purchase of 10 bags of cookies at €2.99 per bag with an expiration date of December 31, 2024.

```python
python superpy.py buy --product_name Cookie --quantity 10 --price 2.99 --expiration_date 2024-12-31
```

Notes:
- If the specified product does not exist in the inventory, it will be added automatically.
- If the specified expiration date is in the past, a warning message will be displayed. The sale will not be recorded


## Sell
The sell command allows you to record the sale of products from your inventory. 

- --product_name: Specify the name of the product you're selling.
- --quantity: Specify the quantity of the product you're selling.
- --price: Specify the price per unit of the product.


#### Usage

```python
python superpy.py sell --product_name <your product name> --quantity <your quantity> --price <your price> 
```

#### Example
This will record a sale of 5 bags of cookies at €3.50 per bag with the closest expiration date.


```python
python superpy.py sell --product_name Cookie --quantity 5 --price 3.50 
```

Notes:
- If the product is not in stock or there is not enough quantity, an error message will be displayed.
- Successful sales will be recorded, and you will receive a confirmation message.


## Report
The report command offers insights into your inventory, revenue, and profit. 

- Inventory: See a detailed list of products in stock.
- Revenue: Get the total income from product sales in a specified time frame.
- Profit: Assess the overall profit from your product transactions.

## Inventory
The --inventory option provides a detailed list of all products in your inventory. To tailor the results, you can specify whether you want to see 'buy' or 'sell' transactions. However, it's essential to include the start and end dates to filter the inventory data accurately.

- -- inventory-type: Specify the choice between buy or sell
- -- start-date: Specify the start date
- -- end-date: Specify the end date

### Usage

```python
python superpy.py report inventory --inventory-type <buy/sell> --start-date <your start date in YYYY-MM-DD format> --end-date <your end date in YYYY-MM-DD format> 
```
### Example
This command will display a list of all products bought between October 2, 2023, and October 31, 2023:

```python
python superpy.py report inventory --inventory-type buy --start-date 2023-10-02 --end-date 2023-10-31
```

Notes:
- The output will be presented into a clear and organized table
- Emphasize that specifying a date range is crucial for obtaining meaningful insights into inventory transactions.
- Remind users to follow the "YYYY-MM-DD" format for both start and end dates.
- Clarify that users can choose between 'buy' and 'sell' to focus on specific transaction types.

## Revenue
The revenue report provides an overview of the total income generated from product sales within a specified time frame.

- -- date: Specify the date


### Usage
```python
python superpy.py report revenue --date <your date in YYYY-MM-DD format> 
```

### Example
To see the revenue for December 31, 2023 you can use:

```python
python superpy.py report revenue --date 2023-12-31 
```

## Profit
The profit report provides an overview of the total profit earned from product sales within a specified time frame.

- -- plot-profit: Use this option to visualize the profit over time.
- -- start-date: Specify the start date
- -- end-date: Specify the end date

- -- date: Specify the date


## Usage

```python
python superpy.py report profit --plot-profit --start-date <your start date in YYYY-MM-DD format> --end-date <your end date in YYYY-MM-DD format> 
```
or 

```python
python superpy.py report profit --date <your date in YYYY-MM-DD format> 
```

## Example 
In the example below, you will see a chart displaying the profit over time.

```python
python superpy.py report profit --plot-profit --start-date 2023-10-09 --end-date 2023-10-15
```

In the following example, you will receive the result without a graphical representation.

```python
python superpy.py report profit --date 2023-10-09
```

Notes:
- When utilizing the '--plot-profit' option, a message will prompt in the terminal, guiding the user to press 'Enter' to proceed. This notification is displayed to prevent the chart from closing prematurely.

## Help function
You can access the help function via the command line by using the --help or -h flag. For example:

```python
 python superpy.py --help
 ```

## Usage
There are three main subcommands: buy, sell, and report. To see more information about each subcommand, you can use:

 ```python
  python superpy.py buy --help
  python superpy.py sell --help
  python superpy.py report --help
  ```

The report subcommand has additional commands like inventory, revenue, and profit. To get specific help for these commands, use:

   ```python
  python superpy.py report inventory --help
  python superpy.py report revenue --help  
  python superpy.py report profit --help  
  ```
