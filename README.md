# ✅ 365 Days To-Do List

A clean, human-friendly command-line To-Do app built in Python.
No frameworks. No databases. Just you, your tasks, and your terminal.

---

## 🚀 Features

| Feature          | Description                                        |
| ---------------- | -------------------------------------------------- |
| ➕ Add tasks      | Name, priority, due date, note, and tags           |
| ✓ Mark done      | Complete tasks with a timestamp                    |
| ✏️ Edit tasks    | Update any field of an existing task               |
| 🗑️ Delete tasks | Remove tasks you no longer need                    |
| 🔍 Search        | Find tasks by name, note, or tag                   |
| 🎛️ Filter       | View by priority, status, due date, or tag         |
| 🔃 Sort          | Arrange by priority, name, due date, or date added |
| 🎯 Focus mode    | Show only high & medium priority pending tasks     |
| 📊 Stats         | Progress bar, breakdown, and tag overview          |
| 📄 Export        | Save your task list to a readable `.txt` file      |
| ↩️ Undo          | Revert the last change (up to 20 steps)            |
| 🏷️ Tags         | Organize tasks with custom labels                  |
| 💾 Auto-save     | Data is saved automatically to `tasks.json`        |

---

## 🧑‍💻 How to Use

### 1. Clone the repository

```bash
git clone https://github.com/your-username/365-days-todo.git
cd 365-days-todo
```

### 2. Run the program

```bash
python main.py
```

### 3. Use the menu

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

## 💡 Example Session

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
  Add a note? (optional): Chapters 3–6
  Tags? (e.g. work python): school

  Added! 'Study for exam' is on your list. Tagged: #school

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

## ⚡ Priority Levels

| Symbol | Level  |
| ------ | ------ |
| 🔴     | High   |
| 🟡     | Medium |
| 🟢     | Low    |

---

## 🧱 Task Data Structure

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

## 📝 Notes

* Tasks are stored in `tasks.json` (auto-created).
* Export creates `tasks_export.txt`.
* Undo keeps up to 20 steps (resets after closing the app).
* Completed tasks appear with ~~strikethrough~~ in the terminal.
* No external dependencies — only Python standard library.

---

## 📈 Changelog

### v4.0 — March 19, 2026

* 🏷️ Tags system (create, search, filter, stats)
* 🎯 Focus mode for priority tasks
* 📄 Export to `.txt`
* ↩️ Undo system (20-step stack)
* 💬 Smart startup message
* 🔍 Search includes tags

### v3.0 — March 18, 2026

* ✏️ Edit tasks
* 🔍 Search (name + notes)
* 🎛️ Filter system
* 🔃 Sorting options
* 📊 Stats dashboard
* 💬 Notes field
* 🕐 Timestamps

### v2.0

* 💾 JSON storage
* 🎨 Priority system
* 📅 Due dates
* 🗑️ Delete tasks
* 🧹 Clear completed

### v1.0

* ➕ Add tasks
* ✓ Mark complete
* 👀 View list

---

## 📜 License

Open-source and free to use.
Go build something great 🚀
