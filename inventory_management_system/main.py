from abc import ABC, abstractmethod
from datetime import date
import json

# Custom exceptions for specific error handling
class InsufficientStockError(Exception):
    """Raised when attempting to sell more stock than available."""
    pass

class DuplicateProductIdError(Exception):
    """Raised when adding a product with an existing ID."""
    pass

class InvalidProductDataError(Exception):
    """Raised when loading invalid product data from file."""
    pass

# Abstract base class for all products
class Product(ABC):
    """Abstract base class representing a generic product."""
    def __init__(self, product_id, name, price, quantity_in_stock):
        self._product_id = product_id          # Protected attribute for product ID
        self._name = name                      # Protected attribute for product name
        self._price = price                    # Protected attribute for price
        self._quantity_in_stock = quantity_in_stock  # Protected attribute for stock quantity

    def restock(self, amount):
        """Increase the stock quantity by the specified amount."""
        if amount < 0:
            raise ValueError("Restock amount cannot be negative")
        self._quantity_in_stock += amount

    def sell(self, quantity):
        """Decrease the stock quantity by the specified amount, with stock check."""
        if quantity < 0:
            raise ValueError("Sell quantity cannot be negative")
        if quantity > self._quantity_in_stock:
            raise InsufficientStockError(f"Not enough stock to sell {quantity} units of {self._name}")
        self._quantity_in_stock -= quantity

    def get_total_value(self):
        """Calculate the total value of the product in stock."""
        return self._price * self._quantity_in_stock

    @abstractmethod
    def __str__(self):
        """Abstract method to return a string representation of the product."""
        pass

    def to_dict(self):
        """Convert product attributes to a dictionary for JSON serialization."""
        return {
            "type": type(self).__name__,
            "product_id": self._product_id,
            "name": self._name,
            "price": self._price,
            "quantity_in_stock": self._quantity_in_stock
        }

# Subclass for electronics products
class Electronics(Product):
    """Class representing an electronics product with warranty and brand."""
    def __init__(self, product_id, name, price, quantity_in_stock, warranty_years, brand):
        super().__init__(product_id, name, price, quantity_in_stock)
        self._warranty_years = warranty_years  # Additional attribute for warranty period
        self._brand = brand                    # Additional attribute for brand name

    def __str__(self):
        """Return a string representation of the electronics product."""
        return (f"Electronics: ID={self._product_id}, Name={self._name}, Price={self._price}, "
                f"Stock={self._quantity_in_stock}, Warranty={self._warranty_years} years, Brand={self._brand}")

    def to_dict(self):
        """Convert electronics product attributes to a dictionary."""
        data = super().to_dict()
        data["warranty_years"] = self._warranty_years
        data["brand"] = self._brand
        return data

    @classmethod
    def from_dict(cls, data):
        """Create an Electronics instance from a dictionary."""
        return cls(
            product_id=data["product_id"],
            name=data["name"],
            price=data["price"],
            quantity_in_stock=data["quantity_in_stock"],
            warranty_years=data["warranty_years"],
            brand=data["brand"]
        )

# Subclass for grocery products
class Grocery(Product):
    """Class representing a grocery product with an expiry date."""
    def __init__(self, product_id, name, price, quantity_in_stock, expiry_date):
        super().__init__(product_id, name, price, quantity_in_stock)
        self._expiry_date = expiry_date        # Additional attribute for expiry date

    def is_expired(self):
        """Check if the grocery product has expired."""
        return date.today() > self._expiry_date

    def __str__(self):
        """Return a string representation of the grocery product."""
        return (f"Grocery: ID={self._product_id}, Name={self._name}, Price={self._price}, "
                f"Stock={self._quantity_in_stock}, Expiry={self._expiry_date}, Expired={self.is_expired()}")

    def to_dict(self):
        """Convert grocery product attributes to a dictionary."""
        data = super().to_dict()
        data["expiry_date"] = self._expiry_date.isoformat()
        return data

    @classmethod
    def from_dict(cls, data):
        """Create a Grocery instance from a dictionary."""
        expiry_date = date.fromisoformat(data["expiry_date"])
        return cls(
            product_id=data["product_id"],
            name=data["name"],
            price=data["price"],
            quantity_in_stock=data["quantity_in_stock"],
            expiry_date=expiry_date
        )

# Subclass for clothing products
class Clothing(Product):
    """Class representing a clothing product with size and material."""
    def __init__(self, product_id, name, price, quantity_in_stock, size, material):
        super().__init__(product_id, name, price, quantity_in_stock)
        self._size = size                      # Additional attribute for size
        self._material = material              # Additional attribute for material

    def __str__(self):
        """Return a string representation of the clothing product."""
        return (f"Clothing: ID={self._product_id}, Name={self._name}, Price={self._price}, "
                f"Stock={self._quantity_in_stock}, Size={self._size}, Material={self._material}")

    def to_dict(self):
        """Convert clothing product attributes to a dictionary."""
        data = super().to_dict()
        data["size"] = self._size
        data["material"] = self._material
        return data

    @classmethod
    def from_dict(cls, data):
        """Create a Clothing instance from a dictionary."""
        return cls(
            product_id=data["product_id"],
            name=data["name"],
            price=data["price"],
            quantity_in_stock=data["quantity_in_stock"],
            size=data["size"],
            material=data["material"]
        )

# Class to manage the inventory
class Inventory:
    """Class to manage a collection of products."""
    def __init__(self):
        self._products = {}  # Dictionary to store products with product_id as key

    def add_product(self, product: Product):
        """Add a product to the inventory."""
        if product._product_id in self._products:
            raise DuplicateProductIdError(f"Product ID {product._product_id} already exists")
        self._products[product._product_id] = product

    def remove_product(self, product_id):
        """Remove a product from the inventory by ID."""
        if product_id not in self._products:
            raise ValueError("Product ID not found")
        del self._products[product_id]

    def search_by_name(self, name):
        """Search for products by name (returns a list)."""
        return [product for product in self._products.values() if product._name == name]

    def search_by_type(self, product_type):
        """Search for products by type (e.g., 'Electronics')."""
        return [product for product in self._products.values() if type(product).__name__ == product_type]

    def list_all_products(self):
        """Return a list of all products in the inventory."""
        return list(self._products.values())

    def sell_product(self, product_id, quantity):
        """Sell a specified quantity of a product."""
        if product_id not in self._products:
            raise ValueError("Product ID not found")
        self._products[product_id].sell(quantity)

    def restock_product(self, product_id, quantity):
        """Restock a specified quantity of a product."""
        if product_id not in self._products:
            raise ValueError("Product ID not found")
        self._products[product_id].restock(quantity)

    def total_inventory_value(self):
        """Calculate the total value of all products in the inventory."""
        return sum(product.get_total_value() for product in self._products.values())

    def remove_expired_products(self):
        """Remove all expired grocery products and return the count."""
        expired_ids = [product._product_id for product in self._products.values() 
                       if isinstance(product, Grocery) and product.is_expired()]
        for product_id in expired_ids:
            del self._products[product_id]
        return len(expired_ids)

    def save_to_file(self, filename):
        """Save the inventory to a JSON file."""
        data = [product.to_dict() for product in self._products.values()]
        with open(filename, 'w') as f:
            json.dump(data, f)

    def load_from_file(self, filename):
        """Load the inventory from a JSON file."""
        with open(filename, 'r') as f:
            data = json.load(f)
        self._products = {}
        product_classes = {
            "Electronics": Electronics,
            "Grocery": Grocery,
            "Clothing": Clothing
        }
        for item in data:
            product_type = item["type"]
            if product_type not in product_classes:
                raise ValueError(f"Unknown product type: {product_type}")
            cls = product_classes[product_type]
            product = cls.from_dict(item)
            self.add_product(product)

# Interactive CLI menu
def main():
    """Main function to run the inventory management system CLI."""
    inventory = Inventory()
    while True:
        print("\nInventory Management System")
        print("1. Add product")
        print("2. Sell product")
        print("3. Search product by name")
        print("4. Search product by type")
        print("5. List all products")
        print("6. Restock product")
        print("7. Remove expired products")
        print("8. Save inventory to file")
        print("9. Load inventory from file")
        print("10. Exit")
        choice = input("Enter your choice: ")

        try:
            if choice == "1":
                product_type = input("Enter product type (Electronics/Grocery/Clothing): ")
                product_id = input("Enter product ID: ")
                name = input("Enter product name: ")
                price = float(input("Enter product price: "))
                quantity_in_stock = int(input("Enter quantity in stock: "))
                if product_type == "Electronics":
                    warranty_years = int(input("Enter warranty years: "))
                    brand = input("Enter brand: ")
                    product = Electronics(product_id, name, price, quantity_in_stock, warranty_years, brand)
                elif product_type == "Grocery":
                    expiry_date_str = input("Enter expiry date (YYYY-MM-DD): ")
                    expiry_date = date.fromisoformat(expiry_date_str)
                    product = Grocery(product_id, name, price, quantity_in_stock, expiry_date)
                elif product_type == "Clothing":
                    size = input("Enter size: ")
                    material = input("Enter material: ")
                    product = Clothing(product_id, name, price, quantity_in_stock, size, material)
                else:
                    print("Invalid product type")
                    continue
                inventory.add_product(product)
                print("Product added successfully")

            elif choice == "2":
                product_id = input("Enter product ID: ")
                quantity = int(input("Enter quantity to sell: "))
                inventory.sell_product(product_id, quantity)
                print("Product sold successfully")

            elif choice == "3":
                name = input("Enter product name to search: ")
                products = inventory.search_by_name(name)
                if products:
                    for product in products:
                        print(product)
                else:
                    print("No products found")

            elif choice == "4":
                product_type = input("Enter product type (Electronics/Grocery/Clothing): ")
                products = inventory.search_by_type(product_type)
                if products:
                    for product in products:
                        print(product)
                else:
                    print("No products found")

            elif choice == "5":
                products = inventory.list_all_products()
                if products:
                    for product in products:
                        print(product)
                else:
                    print("Inventory is empty")

            elif choice == "6":
                product_id = input("Enter product ID: ")
                quantity = int(input("Enter quantity to restock: "))
                inventory.restock_product(product_id, quantity)
                print("Product restocked successfully")

            elif choice == "7":
                removed_count = inventory.remove_expired_products()
                print(f"{removed_count} expired products removed")

            elif choice == "8":
                filename = input("Enter filename to save: ")
                inventory.save_to_file(filename)
                print("Inventory saved successfully")

            elif choice == "9":
                filename = input("Enter filename to load: ")
                inventory.load_from_file(filename)
                print("Inventory loaded successfully")

            elif choice == "10":
                print("Exiting...")
                break

            else:
                print("Invalid choice")

        except (ValueError, InsufficientStockError, DuplicateProductIdError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()