# Inventory Management System

A Python-based OOP (Object-Oriented Programming) application for managing inventory — including products, stock tracking, sales processing, and JSON-based data persistence.

## Features

- Manage Electronics, Grocery, and Clothing products.
- Restock, sell, and search products by name or type.
- Calculate total inventory value and remove expired groceries.
- Interactive CLI menu for easy operation.
- Save/load inventory to/from JSON files.

## Usage

**Requirements:** Python 3.x (no external libraries needed)  
**Run the Program:**
```bash
python inventory_management_system.py

CLI Menu Options

    Add Product – Choose product type (Electronics, Grocery, or Clothing) and enter ID, name, price, stock, and type-specific details.
    Example: Add Electronics → ID: E001, Name: Laptop, Price: 999.99, Stock: 10, Warranty: 2 years, Brand: TechCorp

    Sell Product – Enter product ID and quantity to sell.
    Example: ID: E001, Quantity: 2

    Search by Name – Enter product name to view matching products.

    Search by Type – Enter type (Electronics, Grocery, or Clothing) to list products.

    List All Products – Display all products in inventory.

    Restock Product – Enter product ID and quantity to restock.
    Example: ID: E001, Quantity: 5

    Remove Expired Products – Remove all expired Grocery items.

    Save to File – Enter filename (e.g., inventory.json) to save inventory.

    Load from File – Enter filename to load inventory.

    Exit – Close the program.
