class MenuItem:
    """Represents an individual food item on the menu."""
    def __init__(self, item_id: int, name: str, price: float):
        self.item_id = item_id
        self.name = name
        self.price = price

    def __str__(self):
        return f"[{self.item_id}] {self.name:<20} ${self.price:.2f}"


class Menu:
    """Manages the collection of menu items available."""
    def __init__(self):
        self.items = {}

    def add_item(self, item: MenuItem):
        self.items[item.item_id] = item

    def display_menu(self):
        print("\n=== RESTAURANT MENU ===")
        if not self.items:
            print("The menu is currently empty.")
        for item in self.items.values():
            print(item)
        print("=======================")

    def get_item(self, item_id: int) -> MenuItem:
        return self.items.get(item_id)


class Order:
    """Tracks a customer's specific order, calculating items and totals."""
    def __init__(self, order_id: int):
        self.order_id = order_id
        self.ordered_items = {}  # Format: {MenuItem: quantity}
        self.status = "Pending"

    def add_item(self, item: MenuItem, quantity: int = 1):
        if quantity <= 0:
            print("Quantity must be greater than 0.")
            return
        if item in self.ordered_items:
            self.ordered_items[item] += quantity
        else:
            self.ordered_items[item] = quantity
        print(f"Added {quantity}x {item.name} to Order #{self.order_id}.")

    def calculate_total(self, tax_rate: float = 0.08) -> float:
        subtotal = sum(item.price * qty for item, qty in self.ordered_items.items())
        tax = subtotal * tax_rate
        return subtotal + tax

    def display_receipt(self):
        print(f"\n--- RECEIPT FOR ORDER #{self.order_id} ---")
        print(f"Status: {self.status}")
        if not self.ordered_items:
            print("No items in this order.")
            return
            
        subtotal = 0
        for item, qty in self.ordered_items.items():
            cost = item.price * qty
            subtotal += cost
            print(f"{item.name:<20} x{qty:<3} ${cost:.2f}")
        
        tax = subtotal * 0.08
        total = subtotal + tax
        print("-" * 34)
        print(f"Subtotal:                      ${subtotal:.2f}")
        print(f"Tax (8%):                      ${tax:.2f}")
        print(f"Total Amount Due:              ${total:.2f}")
        print("-" * 34)


class Restaurant:
    """The central Orchestrator managing both the Menu and current Orders."""
    def __init__(self, name: str):
        self.name = name
        self.menu = Menu()
        self.orders = {}
        self._order_id_counter = 1001

    def create_new_order(self) -> Order:
        new_order = Order(self._order_id_counter)
        self.orders[self._order_id_counter] = new_order
        self._order_id_counter += 1
        return new_order


# --- System Simulation / Execution ---
if __name__ == "__main__":
    # Initialize the restaurant
    my_restaurant = Restaurant("Gourmet Express")

    # Populate the menu
    my_restaurant.menu.add_item(MenuItem(1, "Cheeseburger", 8.99))
    my_restaurant.menu.add_item(MenuItem(2, "Veggie Pizza", 12.49))
    my_restaurant.menu.add_item(MenuItem(3, "Caesar Salad", 7.50))
    my_restaurant.menu.add_item(MenuItem(4, "French Fries", 3.99))
    my_restaurant.menu.add_item(MenuItem(5, "Soft Drink", 1.99))

    # Simulate a customer application loop
    print(f"Welcome to {my_restaurant.name}!")
    customer_order = my_restaurant.create_new_order()

    while True:
        my_restaurant.menu.display_menu()
        print("\nOptions: [1] Add Item [2] View Receipt & Checkout [3] Cancel & Exit")
        choice = input("Select an option: ").strip()

        if choice == "1":
            try:
                id_choice = int(input("Enter Item ID to order: "))
                menu_item = my_restaurant.menu.get_item(id_choice)
                
                if menu_item:
                    qty = int(input(f"How many units of '{menu_item.name}'? "))
                    customer_order.add_item(menu_item, qty)
                else:
                    print("Invalid Item ID. Please choose an item from the menu.")
            except ValueError:
                print("Error: Please enter numbers only.")

        elif choice == "2":
            customer_order.display_receipt()
            if customer_order.ordered_items:
                confirm = input("Confirm payment and place order? (yes/no): ").lower()
                if confirm == 'yes':
                    customer_order.status = "Completed"
                    print("\nThank you! Your order has been sent to the kitchen.")
                    break
            else:
                print("Cannot checkout an empty order.")

        elif choice == "3":
            print("Order cancelled. Goodbye!")
            break
        else:
            print("Invalid choice selection. Try again.")
