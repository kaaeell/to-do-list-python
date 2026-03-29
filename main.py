import json
import os
import copy
from datetime import datetime

SAVE_FILE   = "tasks.json"
EXPORT_FILE = "tasks_export.txt"

PRIORITY_COLORS = {
    "high":   "🔴",
    "medium": "🟡",
    "low":    "🟢",
}

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}

# ─── Undo stack ─────────────────────────────────────────────

_undo_stack = []

def snapshot(tasks):
    _undo_stack.append(copy.deepcopy(tasks))
    if len(_undo_stack) > 20:
        _undo_stack.pop(0)

def undo(tasks):
    if not _undo_stack:
        print("  Nothing to undo yet.\n")
        return
    tasks[:] = _undo_stack.pop()
    save_tasks(tasks)
    print("  Done — last change has been undone. ↩️\n")

# ─── Persistence ────────────────────────────────────────────

def load_tasks():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(SAVE_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

# ─── Helpers ────────────────────────────────────────────────

def validate_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except:
        return False

def format_tags(task):
    tags = task.get("tags", [])
    if not tags:
        return ""
    return "  " + "  ".join(f"#{t}" for t in tags)

# ─── Display ────────────────────────────────────────────────

def show_tasks(tasks, label=None):
    if not tasks:
        print("\n  Your list is empty 😄\n")
        return

    print(f"\n  {label}" if label else "\n  Your tasks:\n")

    for i, task in enumerate(tasks, 1):
        done_mark = "✓" if task["done"] else " "
        priority  = PRIORITY_COLORS.get(task["priority"], "⚪")

        due = ""
        if task.get("due"):
            due = f" (due: {task['due']})"
            try:
                due_date = datetime.strptime(task["due"], "%Y-%m-%d")
                if due_date < datetime.now() and not task["done"]:
                    due += " ⚠️ OVERDUE"
            except:
                pass

        note = f" 💬 {task['note']}" if task.get("note") else ""
        tags = format_tags(task)

        name = task["name"]
        if task["done"]:
            name = f"\033[9m{name}\033[0m"

        print(f"  [{done_mark}] {i}. {priority} {name}{due}{note}{tags}")
    print()

# ─── Actions ────────────────────────────────────────────────

def _parse_tags(raw):
    return [t.strip().lstrip("#").lower() for t in raw.replace(",", " ").split() if t.strip()]

def add_task(tasks):
    name = input("  Task name: ").strip()
    if not name:
        print("  Empty task.\n")
        return

    print("  Priority: [1] High  [2] Medium  [3] Low")
    choice   = input("  → ").strip()
    priority = {"1": "high", "3": "low"}.get(choice, "medium")

    due = input("  Due date (YYYY-MM-DD or blank): ").strip()
    if due and not validate_date(due):
        print("  Invalid date format. Use YYYY-MM-DD.\n")
        return

    note     = input("  Note (optional): ").strip()
    raw_tags = input("  Tags: ").strip()
    tags     = _parse_tags(raw_tags)

    snapshot(tasks)

    tasks.append({
        "name": name,
        "priority": priority,
        "due": due,
        "note": note,
        "tags": tags,
        "done": False,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "completed": None,
    })

    save_tasks(tasks)
    print("  Task added!\n")

def mark_done(tasks):
    show_tasks(tasks)
    try:
        idx = int(input("  Task number: ")) - 1
        if 0 <= idx < len(tasks):
            snapshot(tasks)
            tasks[idx]["done"] = True
            tasks[idx]["completed"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            save_tasks(tasks)
            print("  Completed!\n")
    except:
        print("  Invalid input.\n")

def delete_task(tasks):
    show_tasks(tasks)
    try:
        idx = int(input("  Task number: ")) - 1
        if 0 <= idx < len(tasks):
            snapshot(tasks)
            tasks.pop(idx)
            save_tasks(tasks)
            print("  Deleted.\n")
    except:
        print("  Invalid input.\n")

# ─── Main ───────────────────────────────────────────────────

MENU = """
  [1] View tasks
  [2] Add task
  [3] Mark done
  [4] Delete task
  [u] Undo
  [q] Quit
"""

def main():
    tasks = load_tasks()

    print("\n  ✅ To-Do List\n")

    while True:
        print(MENU)
        choice = input("  → ").strip().lower()

        if choice == "1":
            show_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            mark_done(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "u":
            undo(tasks)
        elif choice == "q":
            print("  Bye 👋\n")
            break
        else:
            print("  Invalid option.\n")

if __name__ == "__main__":
    main()
