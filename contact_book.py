contacts = []

while True:
    print("\n===== Contact Book =====")
    print("1. Add Contact")
    print("2. View Contacts")
    print("3. Search Contact")
    print("4. Update Contact")
    print("5. Delete Contact")
    print("6. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        name = input("Enter Name: ")
        phone = input("Enter Phone: ")

        contacts.append({
            "name": name,
            "phone": phone
        })

        print("Contact Added Successfully!")

    elif choice == "2":
        if not contacts:
            print("No Contacts Found")
        else:
            print("\nContact List")
            for i, contact in enumerate(contacts, start=1):
                print(f"{i}. {contact['name']} - {contact['phone']}")

    elif choice == "3":
        search = input("Enter Name: ")
        found = False

        for contact in contacts:
            if contact["name"].lower() == search.lower():
                print(contact["name"], "-", contact["phone"])
                found = True
                break

        if not found:
            print("Contact Not Found")

    elif choice == "4":
        search = input("Enter Contact Name to Update: ")

        for contact in contacts:
            if contact["name"].lower() == search.lower():
                contact["phone"] = input("Enter New Phone: ")
                print("Updated Successfully")
                break
        else:
            print("Contact Not Found")

    elif choice == "5":
        delete = input("Enter Contact Name to Delete: ")

        for contact in contacts:
            if contact["name"].lower() == delete.lower():
                contacts.remove(contact)
                print("Deleted Successfully")
                break
        else:
            print("Contact Not Found")

    elif choice == "6":
        print("Goodbye!")
        break

    else:
        print("Invalid Choice")