# Report

## 1. Dynamic Plotting of Profit Over Time
In the report class, I implemented a dynamic plotting feature that allows users to visualize the profit over a specified time range. The plot_profit method takes start and end dates, fetches the profit data for each day in the range, and plots it using matplotlib. This feature provides a quick and visual way for users to understand the profit trends over a specific period. I chose this implementation to enhance the user experience and provide a more intuitive understanding of financial data.

## 2. Product Inventory Tracking with Differentiation
The inventory method in the report class tracks and displays the product inventory, distinguishing between purchased (buy) and sold (sell) products. This allows users to see the current status of each product in the inventory. The differentiation helps in understanding the stock levels for different products and making informed decisions. I implemented this feature to provide users with detailed insights into their inventory management.

## 3. Error Handling in Selling Process
In the sell class, I implemented an error-checking mechanism within the check_stock method to ensure that a product is in stock before a sale is recorded. This prevents users from selling products that are not available or have insufficient quantity. The implementation uses the check_stock method before recording a sale, and if the stock is insufficient, it prints an error message. This feature enhances the robustness of the application, providing a safeguard against unintentional errors in the selling process.
