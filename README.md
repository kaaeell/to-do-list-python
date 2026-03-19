# ✅ 365 Days To-Do List

A clean, human-friendly command-line To-Do app built in Python.
No frameworks. No databases. Just you, your tasks, and a terminal.

---

## Features

| Feature | Description |
|---|---|
| ➕ Add tasks | Name, priority, due date, note, and tags |
| ✓  Mark done | Check off tasks with a timestamp |
| ✏️  Edit tasks | Update any field on an existing task |
| 🗑️  Delete tasks | Remove a task you no longer need |
| 🔍 Search | Find tasks by name, note, or tag |
| 🎛️  Filter | View by priority, status, due date, or tag |
| 🔃 Sort | Arrange by priority, name, due date, or date added |
| 🎯 Focus mode | See only your high & medium priority pending tasks |
| 📊 Stats | Progress bar + full breakdown + tag cloud |
| 📄 Export | Save your full list to a readable `.txt` file |
| ↩️  Undo | Roll back the last change, up to 20 steps |
| 🏷️  Tags | Label tasks with custom tags and filter by them |
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

  [f] Focus mode          [e] Export to file
  [u] Undo last change    [q] Quit
```

---

## Example Session

```
  ✅ To-Do List
  Thursday, March 19
  ─────────────────────────
  You've got 2 high-priority task(s) waiting. You got this 💪

  → 2
  Task name: Study for exam
  Priority: [1] High  [2] Medium  [3] Low  (default: medium)
  → 1
  Due date? (e.g. Jan 30 or leave blank): Mar 21
  Add a note? (optional, press Enter to skip): Chapters 3–6
  Tags? (e.g. work python — space or comma separated, or leave blank): school
  Added! 'Study for exam' is on your list.  Tagged: #school

  → f
  ── 🎯 Focus Mode ────────────────────────────────────────
  Just the things that actually need your attention today:

  1. 🔴 Study for exam  (due: Mar 21)  #school
     💬 Chapters 3–6
  ─────────────────────────────────────────────────────────

  → u
  Done — last change has been undone. ↩️
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

```json
{
  "name": "Study for exam",
  "priority": "high",
  "due": "Mar 21",
  "note": "Chapters 3–6",
  "tags": ["school"],
  "done": false,
  "created": "2026-03-19 09:15",
  "completed": null
}
```

---

## Notes

- Tasks persist between sessions via `tasks.json` (auto-created in the same folder).
- Export generates `tasks_export.txt` in the same folder.
- Undo keeps up to 20 snapshots in memory — it resets when you quit.
- Completed tasks render with ~~strikethrough~~ in the terminal.
- No external dependencies — standard Python library only.

---

## Changelog

### v4.0 — March 19, 2026
- 🏷️  Added **Tags** — label tasks with custom tags (e.g. `#work`, `#school`), filter and search by them, see a tag cloud in Stats
- 🎯 Added **Focus mode** `[f]` — strips away everything except pending high & medium tasks, so you see only what matters right now
- 📄 Added **Export** `[e]` — writes your full task list to `tasks_export.txt` with all details formatted for reading
- ↩️  Added **Undo** `[u]` — rolls back the last change (add, edit, delete, sort, clear); stacks up to 20 steps in memory
- 💬 Smart launch message — app opens with a nudge based on how many high-priority tasks are waiting
- 🔍 Search now also matches inside tags

### v3.0 — March 18, 2026
- ✏️ Added **Edit task**
- 🔍 Added **Search** (name + notes)
- 🎛️ Added **Filter** (priority, status, due date)
- 🔃 Added **Sort** (priority, name, due date, created)
- 📊 Added **Stats** with progress bar
- 💬 Optional notes per task
- 🕐 Created / completed timestamps

### v2.0
- 💾 JSON persistence
- 🎨 Priority system with emoji indicators
- 📅 Due dates
- 🗑️ Delete tasks
- 🧹 Bulk-clear completed tasks

### v1.0
- ➕ Add tasks
- ✓  Mark as complete
- 👀 View task list
- Menu-driven loop

---

## License

Open-source and free to use. Go build something great :)
