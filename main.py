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

# ─── Undo stack ───────────────────────────────────────────────────────────────

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

def format_tags(task):
    tags = task.get("tags", [])
    if not tags:
        return ""
    return "  " + "  ".join(f"#{t}" for t in tags)

def show_tasks(tasks, label=None):
    if not tasks:
        print("\n  Your list is empty — enjoy the peace while it lasts 😄\n")
        return
    print(f"\n  {label}" if label else "\n  Your tasks:")
    print()
    for i, task in enumerate(tasks, 1):
        done_mark = "✓" if task["done"] else " "
        priority  = PRIORITY_COLORS.get(task["priority"], "⚪")
        due       = f"  (due: {task['due']})" if task.get("due") else ""
        note      = f"  💬 {task['note']}" if task.get("note") else ""
        tags      = format_tags(task)
        name      = task["name"]
        if task["done"]:
            name = f"\033[9m{name}\033[0m"
        print(f"  [{done_mark}] {i}. {priority} {name}{due}{note}{tags}")
    print()

def show_stats(tasks):
    total    = len(tasks)
    done     = sum(1 for t in tasks if t["done"])
    pending  = total - done
    high     = sum(1 for t in tasks if t["priority"] == "high" and not t["done"])
    with_due = sum(1 for t in tasks if t.get("due"))
    pct      = int((done / total) * 100) if total else 0

    bar = "█" * (pct // 5) + "░" * (20 - pct // 5)

    all_tags = []
    for t in tasks:
        all_tags.extend(t.get("tags", []))
    tag_line = "  " + "  ".join(f"#{tg}" for tg in sorted(set(all_tags))) if all_tags else "  none yet"

    print("\n  ─────────────────────────")
    print(f"  📊 Stats — {datetime.now().strftime('%A, %B %d')}")
    print(f"  ─────────────────────────")
    print(f"  Total tasks   : {total}")
    print(f"  ✓  Done        : {done}")
    print(f"  ⏳  Pending     : {pending}")
    print(f"  🔴  High priority pending : {high}")
    print(f"  📅  With due dates        : {with_due}")
    print(f"\n  Progress  [{bar}] {pct}%")
    print(f"\n  🏷️  Tags in use:\n{tag_line}\n")

# ─── Focus mode ───────────────────────────────────────────────────────────────

def focus_mode(tasks):
    focused = [t for t in tasks if not t["done"] and t["priority"] in ("high", "medium")]
    if not focused:
        print("\n  Nothing urgent on your plate — nice place to be 😌\n")
        return
    print("\n  ── 🎯 Focus Mode ────────────────────────────────────────")
    print("  Just the things that actually need your attention today:\n")
    for i, task in enumerate(focused, 1):
        priority = PRIORITY_COLORS.get(task["priority"], "⚪")
        due      = f"  (due: {task['due']})" if task.get("due") else ""
        note     = f"\n     💬 {task['note']}" if task.get("note") else ""
        tags     = format_tags(task)
        print(f"  {i}. {priority} {task['name']}{due}{tags}{note}")
    print("\n  ─────────────────────────────────────────────────────────\n")

# ─── Export ───────────────────────────────────────────────────────────────────

def export_tasks(tasks):
    if not tasks:
        print("  Nothing to export yet.\n")
        return
    lines = [
        f"To-Do List Export — {datetime.now().strftime('%A, %B %d %Y, %H:%M')}",
        "=" * 50,
        "",
    ]
    for i, task in enumerate(tasks, 1):
        status   = "✓ Done" if task["done"] else "  Pending"
        priority = task["priority"].capitalize()
        due      = f"  Due: {task['due']}" if task.get("due") else ""
        note     = f"  Note: {task['note']}" if task.get("note") else ""
        tags     = ("  Tags: " + ", ".join(f"#{tg}" for tg in task.get("tags", []))) if task.get("tags") else ""
        created  = f"  Added: {task.get('created', 'unknown')}"
        lines.append(f"{i}. [{status}] {task['name']}")
        lines.append(f"   Priority: {priority}{due}{note}{tags}{created}")
        if task.get("completed"):
            lines.append(f"   Completed: {task['completed']}")
        lines.append("")

    with open(EXPORT_FILE, "w") as f:
        f.write("\n".join(lines))
    print(f"  Exported {len(tasks)} task(s) to '{EXPORT_FILE}'. 📄\n")

# ─── Actions ──────────────────────────────────────────────────────────────────

def _parse_tags(raw):
    return [t.strip().lstrip("#").lower() for t in raw.replace(",", " ").split() if t.strip()]

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
    raw_tags = input("  Tags? (e.g. work python — space or comma separated, or leave blank): ").strip()
    tags     = _parse_tags(raw_tags)

    snapshot(tasks)
    tasks.append({
        "name":      name,
        "priority":  priority,
        "due":       due,
        "note":      note,
        "tags":      tags,
        "done":      False,
        "created":   datetime.now().strftime("%Y-%m-%d %H:%M"),
        "completed": None,
    })
    save_tasks(tasks)
    tag_hint = f"  Tagged: {', '.join('#' + tg for tg in tags)}" if tags else ""
    print(f"  Added! '{name}' is on your list.{tag_hint}\n")

def mark_done(tasks):
    show_tasks(tasks)
    if not tasks:
        return
    try:
        idx = int(input("  Which task did you finish? (number): ")) - 1
        if 0 <= idx < len(tasks):
            snapshot(tasks)
            tasks[idx]["done"]      = True
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
        print(f"\n  Editing: '{task['name']}' — press Enter to keep the current value.\n")

        new_name = input(f"  Name [{task['name']}]: ").strip()
        if new_name:
            task["name"] = new_name

        print(f"  Priority [{task['priority']}]: [1] High  [2] Medium  [3] Low")
        p = input("  → ").strip()
        if p in ("1", "2", "3"):
            task["priority"] = {"1": "high", "2": "medium", "3": "low"}[p]

        new_due = input(f"  Due date [{task.get('due') or 'none'}]: ").strip()
        if new_due:
            task["due"] = new_due

        new_note = input(f"  Note [{task.get('note') or 'none'}]: ").strip()
        if new_note:
            task["note"] = new_note

        existing_tags = ", ".join(task.get("tags", [])) or "none"
        raw_tags = input(f"  Tags [{existing_tags}]: ").strip()
        if raw_tags:
            task["tags"] = _parse_tags(raw_tags)

        snapshot(tasks)
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
            snapshot(tasks)
            removed = tasks.pop(idx)
            save_tasks(tasks)
            print(f"  Removed '{removed['name']}' from the list.\n")
        else:
            print("  That number doesn't match anything.\n")
    except ValueError:
        print("  Please enter a number.\n")

def clear_done(tasks):
    before = len(tasks)
    snapshot(tasks)
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
    results = [
        t for t in tasks
        if query in t["name"].lower()
        or query in t.get("note", "").lower()
        or query in " ".join(t.get("tags", []))
    ]
    if results:
        show_tasks(results, label=f"Results for '{query}':")
    else:
        print(f"  No tasks match '{query}'.\n")

def filter_tasks(tasks):
    all_tags = sorted(set(tg for t in tasks for tg in t.get("tags", [])))
    print("\n  Filter by:")
    print("  [1] High priority    [4] Pending only")
    print("  [2] Medium priority  [5] Completed only")
    print("  [3] Low priority     [6] Has a due date")
    if all_tags:
        print(f"  [t] Tag  ({', '.join('#' + tg for tg in all_tags)})")
    choice = input("  → ").strip().lower()

    if choice == "t" and all_tags:
        tag     = input("  Which tag? ").strip().lstrip("#").lower()
        results = [t for t in tasks if tag in t.get("tags", [])]
        label   = f"🏷️  Tasks tagged #{tag}:"
    else:
        filters = {
            "1": (lambda t: t["priority"] == "high",   "🔴 High priority:"),
            "2": (lambda t: t["priority"] == "medium",  "🟡 Medium priority:"),
            "3": (lambda t: t["priority"] == "low",     "🟢 Low priority:"),
            "4": (lambda t: not t["done"],               "⏳ Pending:"),
            "5": (lambda t: t["done"],                   "✓ Completed:"),
            "6": (lambda t: bool(t.get("due")),          "📅 With due dates:"),
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
    snapshot(tasks)
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

  [f] Focus mode          [e] Export to file
  [u] Undo last change    [q] Quit
"""

def main():
    tasks   = load_tasks()
    pending = sum(1 for t in tasks if not t["done"])
    high    = sum(1 for t in tasks if t["priority"] == "high" and not t["done"])

    print("\n  ✅ To-Do List")
    print(f"  {datetime.now().strftime('%A, %B %d')}")
    print("  ─────────────────────────")

    if high:
        print(f"  You've got {high} high-priority task(s) waiting. You got this 💪")
    elif pending:
        print(f"  {pending} thing(s) left on your list. Let's knock them out.")
    else:
        print("  All clear! Nothing pending right now 🎉")

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
        "f": lambda: focus_mode(tasks),
        "e": lambda: export_tasks(tasks),
        "u": lambda: undo(tasks),
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
            print("  Hmm, that's not one — try the options above.\n")

if __name__ == "__main__":
    main()
