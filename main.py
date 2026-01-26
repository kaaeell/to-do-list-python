def add_task():
    task = input("Enter task: ")
    task_info = {"task": task, "completed": False}
    tasks.append(task_info)
    print("✅ Task added to the list successfully!\n")


def mark_as_complete():
    if not tasks:
        print("No tasks to mark as complete.\n")
        return

    print("\nTasks:")
    for idx, task in enumerate(tasks, 1):
        status = "✅" if task["completed"] else "❌"
        print(f"{idx}. {task['task']} [{status}]")

    choice = input("Enter the task number to mark as complete: ")

    if not choice.isdigit():
        print("Invalid input. Please enter a number.\n")
        return

    choice = int(choice)
    if 1 <= choice <= len(tasks):
        tasks[choice - 1]["completed"] = True
        print(f"✅ Task '{tasks[choice - 1]['task']}' marked as complete!\n")
    else:
        print("Task number out of range.\n")


def view_tasks():
    if not tasks:
        print("No tasks in the list.\n")
        return

    print("\nTasks:")
    for idx, task in enumerate(tasks, 1):
        status = "✅" if task["completed"] else "❌"
        print(f"{idx}. {task['task']} [{status}]")
    print()


message = """1- Add task to a list
2- Mark task as complete
3- View tasks
4- Quit"""

tasks = []

while True:
    print(message)
    choice = input("Enter your choice: ")

    if choice == "1":
        add_task()
    elif choice == "2":
        mark_as_complete()
    elif choice == "3":
        view_tasks()
    elif choice == "4":
        print("Goodbye!")
        break
    else:
        print("Please choose a number between 1 and 4.\n")
