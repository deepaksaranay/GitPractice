def add_item(items, name, quantity, price):
    items.append({
        "name": name,
        "quantity": quantity,
        "price": price
    })


def find_item(items, name):
    for item in items:
        if item["name"].lower() == name.lower():
            return item
    return None


def update_quantity(items, name, quantity):
    item = find_item(items, name)
    if item is None:
        return False
    item["quantity"] = quantity
    return True


def delete_item(items, name):
    item = find_item(items, name)
    if item is None:
        return False
    items.remove(item)
    return True


def total_inventory_value(items):
    return sum(item["quantity"] * item["price"] for item in items)


def low_stock_items(items, threshold=5):
    return [item for item in items if item["quantity"] < threshold]


if __name__ == "__main__":
    items = []

    while True:
        print("\n===== Inventory Management System =====")
        print("1. Add Item")
        print("2. View Items")
        print("3. Search Item")
        print("4. Update Quantity")
        print("5. Delete Item")
        print("6. Total Inventory Value")
        print("7. Low Stock Report")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter item name: ")
            quantity = int(input("Enter quantity: "))
            price = float(input("Enter price: "))

            add_item(items, name, quantity, price)
            print("Item added successfully!")

        elif choice == "2":
            if len(items) == 0:
                print("No items available.")
            else:
                print("\nItem List")
                for i, item in enumerate(items, start=1):
                    print(f"{i}. {item['name']} - Qty: {item['quantity']} - Price: {item['price']}")

        elif choice == "3":
            search = input("Enter item name: ")
            item = find_item(items, search)

            if item is None:
                print("Item not found.")
            else:
                print(f"Found: {item['name']} - Qty: {item['quantity']} - Price: {item['price']}")

        elif choice == "4":
            name = input("Enter item name: ")
            quantity = int(input("Enter new quantity: "))

            if update_quantity(items, name, quantity):
                print("Quantity updated successfully!")
            else:
                print("Item not found.")

        elif choice == "5":
            name = input("Enter item name to delete: ")

            if delete_item(items, name):
                print("Item deleted successfully!")
            else:
                print("Item not found.")

        elif choice == "6":
            print(f"Total Inventory Value: {total_inventory_value(items)}")

        elif choice == "7":
            low_stock = low_stock_items(items)
            if len(low_stock) == 0:
                print("No low stock items.")
            else:
                print("\nLow Stock Items")
                for i, item in enumerate(low_stock, start=1):
                    print(f"{i}. {item['name']} - Qty: {item['quantity']}")

        elif choice == "8":
            print("Thank you for using Inventory Management System.")
            break

        else:
            print("Invalid choice!")
