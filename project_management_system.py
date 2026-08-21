projects = []

while True:
    print("\n===== Project Management System =====")
    print("1. Add Project")
    print("2. View Projects")
    print("3. Search Project")
    print("4. Add Task to Project")
    print("5. View Tasks")
    print("6. Complete Task")
    print("7. Update Project Status")
    print("8. Delete Project")
    print("9. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        name = input("Enter project name: ")
        description = input("Enter project description: ")

        projects.append({
            "name": name,
            "description": description,
            "status": "Not Started",
            "tasks": []
        })

        print("Project added successfully!")

    elif choice == "2":
        if len(projects) == 0:
            print("No projects available.")
        else:
            print("\nProject List")
            for i, project in enumerate(projects, start=1):
                print(f"{i}. {project['name']} - {project['status']} ({len(project['tasks'])} tasks)")

    elif choice == "3":
        search = input("Enter project name: ")
        found = False

        for project in projects:
            if project["name"].lower() == search.lower():
                print(f"Found: {project['name']} - {project['description']}")
                print(f"Status: {project['status']}")
                print(f"Tasks: {len(project['tasks'])}")
                found = True
                break

        if not found:
            print("Project not found.")

    elif choice == "4":
        if len(projects) == 0:
            print("No projects available.")
        else:
            name = input("Enter project name: ")
            found = False

            for project in projects:
                if project["name"].lower() == name.lower():
                    task = input("Enter task description: ")
                    project["tasks"].append({
                        "description": task,
                        "done": False
                    })
                    print("Task added successfully!")
                    found = True
                    break

            if not found:
                print("Project not found.")

    elif choice == "5":
        if len(projects) == 0:
            print("No projects available.")
        else:
            name = input("Enter project name: ")
            found = False

            for project in projects:
                if project["name"].lower() == name.lower():
                    found = True
                    if len(project["tasks"]) == 0:
                        print("No tasks available for this project.")
                    else:
                        print(f"\nTasks for {project['name']}")
                        for i, task in enumerate(project["tasks"], start=1):
                            status = "Done" if task["done"] else "Pending"
                            print(f"{i}. {task['description']} - {status}")
                    break

            if not found:
                print("Project not found.")

    elif choice == "6":
        if len(projects) == 0:
            print("No projects available.")
        else:
            name = input("Enter project name: ")
            found = False

            for project in projects:
                if project["name"].lower() == name.lower():
                    found = True
                    if len(project["tasks"]) == 0:
                        print("No tasks available for this project.")
                    else:
                        for i, task in enumerate(project["tasks"], start=1):
                            status = "Done" if task["done"] else "Pending"
                            print(f"{i}. {task['description']} - {status}")

                        num = int(input("Enter task number to mark complete: "))
                        if 1 <= num <= len(project["tasks"]):
                            project["tasks"][num - 1]["done"] = True
                            print("Task marked complete!")
                        else:
                            print("Invalid task number.")
                    break

            if not found:
                print("Project not found.")

    elif choice == "7":
        if len(projects) == 0:
            print("No projects available.")
        else:
            name = input("Enter project name: ")
            found = False

            for project in projects:
                if project["name"].lower() == name.lower():
                    print("1. Not Started")
                    print("2. In Progress")
                    print("3. Completed")
                    status_choice = input("Select new status: ")

                    if status_choice == "1":
                        project["status"] = "Not Started"
                    elif status_choice == "2":
                        project["status"] = "In Progress"
                    elif status_choice == "3":
                        project["status"] = "Completed"
                    else:
                        print("Invalid choice.")

                    print("Project status updated!")
                    found = True
                    break

            if not found:
                print("Project not found.")

    elif choice == "8":
        delete = input("Enter project name to delete: ")
        found = False

        for project in projects:
            if project["name"].lower() == delete.lower():
                projects.remove(project)
                print("Project deleted successfully!")
                found = True
                break

        if not found:
            print("Project not found.")

    elif choice == "9":
        print("Thank you for using Project Management System.")
        break

    else:
        print("Invalid choice!")
