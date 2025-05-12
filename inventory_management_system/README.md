Inventory Management System
A Python-based OOP application to manage products, track stock, process sales, and save/load inventory data in JSON format.
Features

Manage Electronics, Grocery, and Clothing products.
Restock, sell, and search products by name or type.
Calculate total inventory value and remove expired groceries.
Interactive CLI menu for easy operation.
Save/load inventory to/from JSON files.

Usage

Requirements: Python 3.x (no external libraries needed).
Run the Program:python inventory_management_system.py


CLI Menu Options:
1. Add Product: Choose product type (Electronics/Grocery/Clothing), enter ID, name, price, stock, and type-specific details (e.g., warranty/brand for Electronics, expiry date for Grocery, size/material for Clothing).
Example: Add Electronics → ID: E001, Name: Laptop, Price: 999.99, Stock: 10, Warranty: 2 years, Brand: TechCorp.


2. Sell Product: Enter product ID and quantity to sell.
Example: ID: E001, Quantity: 2.


3. Search by Name: Enter product name to view matching products.
4. Search by Type: Enter type (Electronics/Grocery/Clothing) to list products.
5. List All Products: Display all products in inventory.
6. Restock Product: Enter product ID and quantity to restock.
Example: ID: E001, Quantity: 5.


7. Remove Expired Products: Remove all expired Grocery items.
8. Save to File: Enter filename (e.g., inventory.json) to save inventory.
9. Load from File: Enter filename to load inventory.
10. Exit: Close the program.

