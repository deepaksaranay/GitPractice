def add_member(members, name):
    if find_member(members, name) is not None:
        return False
    members.append(name)
    return True


def find_member(members, name):
    for member in members:
        if member.lower() == name.lower():
            return member
    return None


def add_expense(expenses, members, description, amount, paid_by, split_among=None):
    payer = find_member(members, paid_by)
    if payer is None or amount <= 0:
        return False

    if split_among is None:
        participants = list(members)
    else:
        participants = []
        for name in split_among:
            member = find_member(members, name)
            if member is None:
                return False
            if member not in participants:
                participants.append(member)

    if len(participants) == 0:
        return False

    expenses.append({
        "description": description,
        "amount": amount,
        "paid_by": payer,
        "split_among": participants
    })
    return True


def split_amount(amount, count):
    # Work in cents so the shares always add back up to the exact amount;
    # leftover cents go to the first participants.
    cents = round(amount * 100)
    base, remainder = divmod(cents, count)
    return [(base + (1 if i < remainder else 0)) / 100 for i in range(count)]


def calculate_balances(members, expenses):
    # Positive balance = is owed money, negative = owes money.
    balances = {member: 0 for member in members}
    for expense in expenses:
        balances[expense["paid_by"]] += round(expense["amount"] * 100)
        shares = split_amount(expense["amount"], len(expense["split_among"]))
        for member, share in zip(expense["split_among"], shares):
            balances[member] -= round(share * 100)
    return {member: cents / 100 for member, cents in balances.items()}


def settle_up(balances):
    # Greedy: repeatedly match the biggest debtor with the biggest creditor.
    creditors = [[name, round(bal * 100)] for name, bal in balances.items() if bal > 0]
    debtors = [[name, round(-bal * 100)] for name, bal in balances.items() if bal < 0]
    creditors.sort(key=lambda c: c[1], reverse=True)
    debtors.sort(key=lambda d: d[1], reverse=True)

    payments = []
    i = j = 0
    while i < len(debtors) and j < len(creditors):
        amount = min(debtors[i][1], creditors[j][1])
        payments.append((debtors[i][0], creditors[j][0], amount / 100))
        debtors[i][1] -= amount
        creditors[j][1] -= amount
        if debtors[i][1] == 0:
            i += 1
        if creditors[j][1] == 0:
            j += 1
    return payments


def total_spent(expenses):
    return round(sum(expense["amount"] for expense in expenses), 2)


if __name__ == "__main__":
    members = []
    expenses = []

    while True:
        print("\n===== Bill Splitter =====")
        print("1. Add Member")
        print("2. View Members")
        print("3. Add Expense")
        print("4. View Expenses")
        print("5. View Balances")
        print("6. Settle Up")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter member name: ").strip()
            if name == "":
                print("Name cannot be empty.")
            elif add_member(members, name):
                print("Member added successfully!")
            else:
                print("Member already exists.")

        elif choice == "2":
            if len(members) == 0:
                print("No members found.")
            else:
                print("\nMember List")
                for i, member in enumerate(members, start=1):
                    print(f"{i}. {member}")

        elif choice == "3":
            if len(members) == 0:
                print("Add members before adding expenses.")
                continue

            description = input("Enter description: ")
            try:
                amount = float(input("Enter amount: "))
            except ValueError:
                print("Invalid amount.")
                continue
            paid_by = input("Paid by: ")
            names = input("Split among (comma-separated, blank for everyone): ").strip()
            split_among = None if names == "" else [n.strip() for n in names.split(",")]

            if add_expense(expenses, members, description, amount, paid_by, split_among):
                print("Expense added successfully!")
            else:
                print("Could not add expense. Check the amount and member names.")

        elif choice == "4":
            if len(expenses) == 0:
                print("No expenses found.")
            else:
                print("\nExpense List")
                for i, expense in enumerate(expenses, start=1):
                    print(f"{i}. {expense['description']} - {expense['amount']:.2f} "
                          f"paid by {expense['paid_by']} "
                          f"(split: {', '.join(expense['split_among'])})")
                print(f"Total Spent: {total_spent(expenses):.2f}")

        elif choice == "5":
            if len(members) == 0:
                print("No members found.")
            else:
                print("\nBalances")
                for member, balance in calculate_balances(members, expenses).items():
                    if balance > 0:
                        print(f"{member} is owed {balance:.2f}")
                    elif balance < 0:
                        print(f"{member} owes {-balance:.2f}")
                    else:
                        print(f"{member} is settled up")

        elif choice == "6":
            payments = settle_up(calculate_balances(members, expenses))
            if len(payments) == 0:
                print("Everyone is settled up.")
            else:
                print("\nPayments to Settle Up")
                for i, (debtor, creditor, amount) in enumerate(payments, start=1):
                    print(f"{i}. {debtor} pays {creditor} {amount:.2f}")

        elif choice == "7":
            print("Thank you for using Bill Splitter.")
            break

        else:
            print("Invalid choice!")
