books = []

while True:
    print("\n===== Library Management System =====")
    print("1. Add Book")
    print("2. View Books")
    print("3. Search Book")
    print("4. Delete Book")
    print("5. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        title = input("Enter book title: ")
        author = input("Enter author name: ")

        books.append({
            "title": title,
            "author": author
        })

        print("Book added successfully!")

    elif choice == "2":
        if len(books) == 0:
            print("No books available.")
        else:
            print("\nBook List")
            for i, book in enumerate(books, start=1):
                print(f"{i}. {book['title']} - {book['author']}")

    elif choice == "3":
        search = input("Enter book title: ")
        found = False

        for book in books:
            if book["title"].lower() == search.lower():
                print(f"Found: {book['title']} by {book['author']}")
                found = True
                break

        if not found:
            print("Book not found.")

    elif choice == "4":
        delete = input("Enter book title to delete: ")
        found = False

        for book in books:
            if book["title"].lower() == delete.lower():
                books.remove(book)
                print("Book deleted successfully!")
                found = True
                break

        if not found:
            print("Book not found.")

    elif choice == "5":
        print("Thank you for using Library Management System.")
        break

    else:
        print("Invalid choice!")