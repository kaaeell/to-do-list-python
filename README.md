# ✅ 365 Days To-Do List

A clean, human-friendly command-line To-Do app built in Python.
No frameworks. No databases. Just you, your tasks, and a terminal.

---

## Features

| Feature | Description |
|---|---|
| ➕ Add tasks | Name, priority, due date, and an optional note |
| ✓  Mark done | Check off tasks with a timestamp |
| ✏️  Edit tasks | Update name, priority, due date, or note anytime |
| 🗑️  Delete tasks | Remove a task you no longer need |
| 🔍 Search | Find tasks by name or note keyword |
| 🎛️  Filter | View by priority, status, or due date |
| 🔃 Sort | Arrange by priority, name, due date, or date added |
| 📊 Stats | See your progress with a visual progress bar |
| 🧹 Clear done | Bulk-remove all completed tasks |
| 💾 Auto-save | Everything saves to `tasks.json` automatically |

---

## How to Use

**1. Clone the repository**
```bash
git clone https://github.com/your-username/365-days-todo.git
cd 365-days-todo
```

**2. Run the program**
```bash
python main.py
```

**3. Use the menu**
```
  What do you want to do?

  [1] View tasks          [6] Search tasks
  [2] Add a task          [7] Filter tasks
  [3] Mark a task done    [8] Sort tasks
  [4] Edit a task         [9] Stats
  [5] Delete a task       [0] Clear completed

  [q] Quit
```

---

## Example Session

```
  ✅ To-Do List
  Wednesday, March 18
  ─────────────────────────

  → 2
  Task name: Finish homework
  Priority: [1] High  [2] Medium  [3] Low  (default: medium)
  → 1
  Due date? (e.g. Jan 30 or leave blank): Mar 20
  Add a note? (optional, press Enter to skip): Chapter 4 only
  Added! 'Finish homework' is on your list.

  → 9
  ─────────────────────────
  📊 Stats — Wednesday, March 18
  ─────────────────────────
  Total tasks   : 1
  ✓  Done        : 0
  ⏳  Pending     : 1
  🔴  High priority pending: 1
  📅  Tasks with due dates : 1

  Progress  [░░░░░░░░░░░░░░░░░░░░] 0%
```

---

## Priority Levels

| Symbol | Level  |
|--------|--------|
| 🔴     | High   |
| 🟡     | Medium |
| 🟢     | Low    |

---

## Task Data Structure

Each task is stored as a JSON object:
```json
{
  "name": "Finish homework",
  "priority": "high",
  "due": "Mar 20",
  "note": "Chapter 4 only",
  "done": false,
  "created": "2026-03-18 10:30",
  "completed": null
}
```

---

## Notes

- Tasks persist between sessions via `tasks.json` (auto-created in the same folder).
- Completed tasks render with ~~strikethrough~~ in the terminal.
- No external dependencies — standard Python library only.

---

## Changelog

### v3.0 — March 2026
- ✏️ Added **Edit task** — update any field without re-adding
- 🔍 Added **Search** — keyword search across name and notes
- 🎛️ Added **Filter** — view tasks by priority, status, or due date
- 🔃 Added **Sort** — reorder by priority, name, due date, or creation date
- 📊 Added **Stats** — progress bar + task breakdown
- 💬 Added **Notes** — attach a short note to any task
- 🕐 Added **Created / Completed timestamps** stored per task
- 🧹 Redesigned menu layout for clarity

### v2.0
- 💾 JSON persistence (tasks survive app restarts)
- 🎨 Priority system with emoji color indicators
- 📅 Due dates per task
- 🗑️ Delete individual tasks
- 🧹 Bulk-clear completed tasks

### v1.0
- ➕ Add tasks
- ✓  Mark as complete
- 👀 View task list
- Menu-driven loop

---

## License

Open-source and free to use. Go build something great :)
