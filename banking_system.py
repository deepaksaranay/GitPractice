accounts = {}

while True:
    print("\n===== BANKING SYSTEM =====")
    print("1. Create Account")
    print("2. Deposit Money")
    print("3. Withdraw Money")
    print("4. Check Balance")
    print("5. View All Accounts")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        name = input("Enter account holder name: ")

        if name in accounts:
            print("Account already exists!")
        else:
            balance = float(input("Enter opening balance: "))
            accounts[name] = balance
            print("Account created successfully!")

    elif choice == "2":
        name = input("Enter account holder name: ")

        if name in accounts:
            amount = float(input("Enter deposit amount: "))
            accounts[name] += amount
            print("Deposit successful!")
            print("Current Balance:", accounts[name])
        else:
            print("Account not found!")

    elif choice == "3":
        name = input("Enter account holder name: ")

        if name in accounts:
            amount = float(input("Enter withdrawal amount: "))

            if amount <= accounts[name]:
                accounts[name] -= amount
                print("Withdrawal successful!")
                print("Current Balance:", accounts[name])
            else:
                print("Insufficient balance!")
        else:
            print("Account not found!")

    elif choice == "4":
        name = input("Enter account holder name: ")

        if name in accounts:
            print("Current Balance:", accounts[name])
        else:
            print("Account not found!")

    elif choice == "5":
        if len(accounts) == 0:
            print("No accounts available.")
        else:
            print("\nAccount List")
            for name, balance in accounts.items():
                print(f"{name} : ₹{balance}")

    elif choice == "6":
        print("Thank you for using Banking System.")
        break

    else:
        print("Invalid choice!")