import json
import os
from datetime import datetime

SAVE_FILE = "tasks.json"

PRIORITY_COLORS = {
    "high":   "🔴",
    "medium": "🟡",
    "low":    "🟢",
}


#persistence

def load_tasks():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    return []


def save_tasks(tasks):
    with open(SAVE_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


#display

def show_tasks(tasks):
    if not tasks:
        print("\n  Your list is empty — enjoy the peace while it lasts 😄\n")
        return

    print("\n  Your tasks:\n")
    for i, task in enumerate(tasks, 1):
        done_mark  = "✓" if task["done"] else " "
        priority   = PRIORITY_COLORS.get(task["priority"], "⚪")
        due        = f"  (due: {task['due']})" if task["due"] else ""
        name       = task["name"]
        if task["done"]:
            name = f"\033[9m{name}\033[0m"   # strikethrough when done
        print(f"  [{done_mark}] {i}. {priority} {name}{due}")
    print()


#actions
def add_task(tasks):
    name = input("  Task name: ").strip()
    if not name:
        print("  Seems empty — try again!\n")
        return

    print("  Priority: [1] High  [2] Medium  [3] Low  (default: medium)")
    choice = input("  → ").strip()
    priority = {"1": "high", "3": "low"}.get(choice, "medium")

    due = input("  Due date? (e.g. Jan 30 or leave blank): ").strip()

    tasks.append({"name": name, "priority": priority, "due": due, "done": False})
    save_tasks(tasks)
    print(f"  Added! '{name}' is on your list.\n")


def mark_done(tasks):
    show_tasks(tasks)
    if not tasks:
        return
    try:
        idx = int(input("  Which task did you finish? (number): ")) - 1
        if 0 <= idx < len(tasks):
            tasks[idx]["done"] = True
            save_tasks(tasks)
            print(f"  Nice work finishing '{tasks[idx]['name']}'! ✓\n")
        else:
            print("  That number doesn't match anything.\n")
    except ValueError:
        print("  Please enter a number.\n")


def delete_task(tasks):
    show_tasks(tasks)
    if not tasks:
        return
    try:
        idx = int(input("  Which task do you want to remove? (number): ")) - 1
        if 0 <= idx < len(tasks):
            removed = tasks.pop(idx)
            save_tasks(tasks)
            print(f"  Removed '{removed['name']}' from the list.\n")
        else:
            print("  That number doesn't match anything.\n")
    except ValueError:
        print("  Please enter a number.\n")


def clear_done(tasks):
    before = len(tasks)
    tasks[:] = [t for t in tasks if not t["done"]]
    after = len(tasks)
    save_tasks(tasks)
    cleaned = before - after
    if cleaned:
        print(f"  Cleaned up {cleaned} completed task(s). Fresh start!\n")
    else:
        print("  No completed tasks to remove.\n")


#main loop

def main():
    tasks = load_tasks()

    print("\n  ✅ To-Do List")
    print(f"  {datetime.now().strftime('%A, %B %d')}")
    print("  ─────────────────────────")

    menu = """
  What do you want to do?
  [1] View tasks
  [2] Add a task
  [3] Mark a task as done
  [4] Delete a task
  [5] Clear completed tasks
  [6] Quit
"""

    while True:
        print(menu)
        choice = input("  → ").strip()

        if choice == "1":
            show_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            mark_done(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            clear_done(tasks)
        elif choice == "6":
            print("\n  See you later! Keep it up 👋\n")
            break
        else:
            print("  Hmm, that's not an option — try 1 through 6.\n")


if __name__ == "__main__":
    main()
