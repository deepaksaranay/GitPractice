students = []

while True:
    print("\n===== Student Management System =====")
    print("1. Add Student")
    print("2. View Students")
    print("3. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        name = input("Enter student name: ")
        marks = int(input("Enter marks: "))
        students.append({"name": name, "marks": marks})
        print("Student added successfully!")

    elif choice == "2":
        if len(students) == 0:
            print("No students found.")
        else:
            for student in students:
                print(student["name"], "-", student["marks"])

    elif choice == "3":
        print("Goodbye!")
        break

    else:
        print("Invalid choice!")