expenses = []

while True:
    print("\n===== Expense Tracker =====")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Total Expense")
    print("4. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        category = input("Enter category: ")
        amount = float(input("Enter amount: "))

        expenses.append({
            "category": category,
            "amount": amount
        })

        print("Expense Added!")

    elif choice == "2":
        if len(expenses) == 0:
            print("No expenses found.")
        else:
            print("\nExpenses:")
            for expense in expenses:
                print(expense["category"], "-", expense["amount"])

    elif choice == "3":
        total = 0

        for expense in expenses:
            total += expense["amount"]

        print("Total Expense =", total)

    elif choice == "4":
        print("Goodbye!")
        break

    else:
        print("Invalid Choice")