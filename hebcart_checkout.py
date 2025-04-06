"""
Importing required libraries to read from JSON files and OS format since I am working in Windows OS
"""

import json
import os

"""
Tax Rate is hardcoded nevertheless this could be changed to another variable
"""
tax_rate = 0.0825  # Sales tax rate of 8.25%

class ShoppingCart:
    def __init__(self, cart_file, coupon_file, tax_rate):
        """
        Initialize the ShoppingCart with tax rate, and load items and coupons from JSON files.
        Stores the original cart to avoid permanent modifications when applying discounts.
        """
        self.original_cart_data = self.load_json(cart_file)
        self.cart_file = cart_file
        self.coupon_file = coupon_file
        self.coupons = self.load_json(coupon_file)
        self.tax_rate = tax_rate

        self.cart = self.orig_copy_cart()  # Use a fresh working copy of cart

        if not self.cart:
            print("Warning: Shopping cart is empty!")

    def load_json(self, file_path):
        """
        Load JSON data from a file and return as a Python list or dict.
        Returns an empty list if the file is missing or contains invalid JSON.
        Including validation for each file and path cart and coupons 
        """
        if not os.path.exists(file_path):
            print(f"Error: {file_path} not found.")
            return []

        with open(file_path, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                print(f"Error: Invalid JSON in {file_path}")
                return []

    def orig_copy_cart(self):
        """
        Return a original copy of the initial cart data.
        """
        return [item.copy() for item in self.original_cart_data]

    def reset_cart(self):
        """
        Resets the cart to its original data before any processing.
        This is required to make it work with the while option of the script
        """
        self.cart = self.orig_copy_cart()

    def calculate_subtotal(self):
        """
        Calculate the subtotal of all items in the cart.
        """
        return sum(item["price"] for item in self.cart)

    def calculate_tax(self, all_taxable=True):
        """
        Calculate the tax total, either assuming all items are taxable
        or using the isTaxable flag in each item.
        """
        if all_taxable:
            return sum(item["price"] * self.tax_rate for item in self.cart)
        else:
            return sum(item["price"] * self.tax_rate for item in self.cart if item.get("isTaxable", True))

    def apply_coupons(self):
        """
        Replace item price with coupon discounted price based on SKU match.
        Ensures that discounted price is not negative.
        """
        coupon_dict = {c["appliedSku"]: c["discountPrice"] for c in self.coupons}

        for item in self.cart:
            if item["sku"] in coupon_dict:
                discounted_price = coupon_dict[item["sku"]]
                item["price"] = max(0, discounted_price)  # Replace price, ensure it's not negative

    def display_totals(self, apply_tax=True, all_taxable=True, use_coupons=False):
        """
        Display subtotal, tax, and grand total. Resets cart each time to ensure clean calculation.
        """
        self.reset_cart()

        if not self.cart:
            print("Your shopping cart is empty. Please add items.")
            return

        if use_coupons:
            self.apply_coupons()

        subtotal = self.calculate_subtotal()
        tax = self.calculate_tax(all_taxable) if apply_tax else 0
        grand_total = subtotal + tax

        print("\n===== Shopping Cart Summary =====")
        print(f"{'Subtotal:':<15} ${subtotal:>7.2f}")
        print(f"{'Tax Total:':<15} ${tax:>7.2f}")
        print(f"{'Grand Total:':<15} ${grand_total:>7.2f}")
        print("=================================\n")


def main():
    # Update these to valid Windows paths where your JSON files are located
    cart_file = r"C:\Users\jetga\Documents\Gitactions\Enrique-Torrentera\cart.json"
    coupon_file = r"C:\Users\jetga\Documents\Gitactions\Enrique-Torrentera\coupons.json"
    """
    # Prompt the user for a tax rate input (e.g., 0.0825 for 8.25%)
    while True:
        try:
            tax_rate_input = input("Please enter the tax rate (e.g., 0.0825 for 8.25%): ")
            tax_rate = float(tax_rate_input)
            if tax_rate < 0:
                raise ValueError("Tax rate cannot be negative.")
            break
        except ValueError:
            print("Invalid input. Please enter a valid decimal number (e.g., 0.0825).")
    """
    # Initialize the shopping cart before each execution
    cart = ShoppingCart(cart_file, coupon_file, tax_rate)

    #  Menu for user interaction
    while True:
        print("\n Shopping Cart Menu ")
        print("1️) Total of the Shopping Cart (No discounts, No taxes)")
        print("2️) Total with Subtotal, Tax Total, and Grand Total (All items taxable)")
        print("3️) Total considering the isTaxable flag in cart.json")
        print("4️) Apply both Taxes and Coupons from coupons.json")
        print("5️) Exit")

        choice = input("Please select an option (1-5): ")

        if choice == "1":
            print("\n🔹 OPTION 1: Subtotal only (No tax, No discounts)")
            cart.display_totals(apply_tax=False)

        elif choice == "2":
            print("\n🔹 OPTION 2: All items taxable")
            cart.display_totals(apply_tax=True, all_taxable=True)

        elif choice == "3":
            print("\n🔹 OPTION 3: Only taxable items contribute to sales tax")
            cart.display_totals(apply_tax=True, all_taxable=False)

        elif choice == "4":
            print("\n🔹 OPTION 4: Apply Taxes and Coupons")
            cart.display_totals(apply_tax=True, all_taxable=False, use_coupons=True)

        elif choice == "5":
            print("\n Exiting Shopping Cart. Goodbye!")
            break

        else:
            print("Invalid option. Please select a number between 1 and 5.")


if __name__ == "__main__":
    main()