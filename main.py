import json
import os
from datetime import datetime

SAVE_FILE = "tasks.json"

PRIORITY_COLORS = {
    "high":   "🔴",
    "medium": "🟡",
    "low":    "🟢",
}

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}

# ─── Persistence ──────────────────────────────────────────────────────────────

def load_tasks():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(SAVE_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

# ─── Display ──────────────────────────────────────────────────────────────────

def show_tasks(tasks, label=None):
    if not tasks:
        print("\n  Your list is empty — enjoy the peace while it lasts 😄\n")
        return
    if label:
        print(f"\n  {label}\n")
    else:
        print("\n  Your tasks:\n")
    for i, task in enumerate(tasks, 1):
        done_mark = "✓" if task["done"] else " "
        priority  = PRIORITY_COLORS.get(task["priority"], "⚪")
        due       = f"  (due: {task['due']})" if task.get("due") else ""
        note      = f"  💬 {task['note']}" if task.get("note") else ""
        name      = task["name"]
        if task["done"]:
            name = f"\033[9m{name}\033[0m"
        print(f"  [{done_mark}] {i}. {priority} {name}{due}{note}")
    print()

def show_stats(tasks):
    total     = len(tasks)
    done      = sum(1 for t in tasks if t["done"])
    pending   = total - done
    high      = sum(1 for t in tasks if t["priority"] == "high" and not t["done"])
    with_due  = sum(1 for t in tasks if t.get("due"))
    pct       = int((done / total) * 100) if total else 0

    bar_filled = pct // 5
    bar = "█" * bar_filled + "░" * (20 - bar_filled)

    print("\n  ─────────────────────────")
    print(f"  📊 Stats — {datetime.now().strftime('%A, %B %d')}")
    print(f"  ─────────────────────────")
    print(f"  Total tasks   : {total}")
    print(f"  ✓  Done        : {done}")
    print(f"  ⏳  Pending     : {pending}")
    print(f"  🔴  High priority pending: {high}")
    print(f"  📅  Tasks with due dates : {with_due}")
    print(f"\n  Progress  [{bar}] {pct}%\n")

# ─── Actions ──────────────────────────────────────────────────────────────────

def add_task(tasks):
    name = input("  Task name: ").strip()
    if not name:
        print("  Seems empty — try again!\n")
        return
    print("  Priority: [1] High  [2] Medium  [3] Low  (default: medium)")
    choice   = input("  → ").strip()
    priority = {"1": "high", "3": "low"}.get(choice, "medium")
    due      = input("  Due date? (e.g. Jan 30 or leave blank): ").strip()
    note     = input("  Add a note? (optional, press Enter to skip): ").strip()
    tasks.append({
        "name":     name,
        "priority": priority,
        "due":      due,
        "note":     note,
        "done":     False,
        "created":  datetime.now().strftime("%Y-%m-%d %H:%M"),
    })
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
            tasks[idx]["completed"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            save_tasks(tasks)
            print(f"  Nice work finishing '{tasks[idx]['name']}'! ✓\n")
        else:
            print("  That number doesn't match anything.\n")
    except ValueError:
        print("  Please enter a number.\n")


def edit_task(tasks):
    show_tasks(tasks)
    if not tasks:
        return
    try:
        idx = int(input("  Which task do you want to edit? (number): ")) - 1
        if not (0 <= idx < len(tasks)):
            print("  That number doesn't match anything.\n")
            return
        task = tasks[idx]
        print(f"\n  Editing: '{task['name']}' — just press Enter to keep current value.\n")

        new_name = input(f"  New name [{task['name']}]: ").strip()
        if new_name:
            task["name"] = new_name

        print(f"  Priority [{task['priority']}]: [1] High  [2] Medium  [3] Low")
        p_choice = input("  → ").strip()
        if p_choice in ("1", "2", "3"):
            task["priority"] = {"1": "high", "2": "medium", "3": "low"}[p_choice]

        new_due = input(f"  Due date [{task.get('due') or 'none'}]: ").strip()
        if new_due:
            task["due"] = new_due

        new_note = input(f"  Note [{task.get('note') or 'none'}]: ").strip()
        if new_note:
            task["note"] = new_note

        save_tasks(tasks)
        print(f"  Updated! '{task['name']}' looks good now.\n")
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
    after   = len(tasks)
    save_tasks(tasks)
    cleaned = before - after
    if cleaned:
        print(f"  Cleaned up {cleaned} completed task(s). Fresh start!\n")
    else:
        print("  No completed tasks to remove.\n")


def search_tasks(tasks):
    query = input("  Search for: ").strip().lower()
    if not query:
        print("  Nothing to search for.\n")
        return
    results = [t for t in tasks if query in t["name"].lower() or query in t.get("note", "").lower()]
    if results:
        show_tasks(results, label=f"Results for '{query}':")
    else:
        print(f"  No tasks match '{query}'.\n")


def filter_tasks(tasks):
    print("\n  Filter by:")
    print("  [1] High priority")
    print("  [2] Medium priority")
    print("  [3] Low priority")
    print("  [4] Pending only")
    print("  [5] Completed only")
    print("  [6] Has a due date")
    choice = input("  → ").strip()
    filters = {
        "1": (lambda t: t["priority"] == "high",   "🔴 High priority tasks:"),
        "2": (lambda t: t["priority"] == "medium",  "🟡 Medium priority tasks:"),
        "3": (lambda t: t["priority"] == "low",     "🟢 Low priority tasks:"),
        "4": (lambda t: not t["done"],               "⏳ Pending tasks:"),
        "5": (lambda t: t["done"],                   "✓ Completed tasks:"),
        "6": (lambda t: bool(t.get("due")),          "📅 Tasks with due dates:"),
    }
    if choice not in filters:
        print("  Not a valid option.\n")
        return
    fn, label = filters[choice]
    results   = [t for t in tasks if fn(t)]
    if results:
        show_tasks(results, label=label)
    else:
        print("  No tasks match that filter.\n")


def sort_tasks(tasks):
    print("\n  Sort by:")
    print("  [1] Priority (high → low)")
    print("  [2] Name (A → Z)")
    print("  [3] Due date")
    print("  [4] Date added")
    choice = input("  → ").strip()
    if choice == "1":
        tasks.sort(key=lambda t: PRIORITY_ORDER.get(t["priority"], 99))
        label = "Sorted by priority:"
    elif choice == "2":
        tasks.sort(key=lambda t: t["name"].lower())
        label = "Sorted A → Z:"
    elif choice == "3":
        tasks.sort(key=lambda t: t.get("due") or "zzz")
        label = "Sorted by due date:"
    elif choice == "4":
        tasks.sort(key=lambda t: t.get("created") or "")
        label = "Sorted by date added:"
    else:
        print("  Not a valid option.\n")
        return
    save_tasks(tasks)
    show_tasks(tasks, label=label)

# ─── Main loop ────────────────────────────────────────────────────────────────

MENU = """
  What do you want to do?

  [1] View tasks          [6] Search tasks
  [2] Add a task          [7] Filter tasks
  [3] Mark a task done    [8] Sort tasks
  [4] Edit a task         [9] Stats
  [5] Delete a task       [0] Clear completed

  [q] Quit
"""

def main():
    tasks = load_tasks()
    print("\n  ✅ To-Do List")
    print(f"  {datetime.now().strftime('%A, %B %d')}")
    print("  ─────────────────────────")

    actions = {
        "1": lambda: show_tasks(tasks),
        "2": lambda: add_task(tasks),
        "3": lambda: mark_done(tasks),
        "4": lambda: edit_task(tasks),
        "5": lambda: delete_task(tasks),
        "6": lambda: search_tasks(tasks),
        "7": lambda: filter_tasks(tasks),
        "8": lambda: sort_tasks(tasks),
        "9": lambda: show_stats(tasks),
        "0": lambda: clear_done(tasks),
    }

    while True:
        print(MENU)
        choice = input("  → ").strip().lower()
        if choice == "q":
            print("\n  See you later! Keep it up 👋\n")
            break
        elif choice in actions:
            actions[choice]()
        else:
            print("  Hmm, that's not an option — try 1 through 9, 0, or q.\n")

if __name__ == "__main__":
    main()
