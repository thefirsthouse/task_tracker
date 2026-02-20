# task_tracker
[text](https://roadmap.sh/projects/task-tracker)

## Getting Started 🚀

1. **(Optional) set up a virtual environment:**
   ```bash
   python3 -m venv env
   source env/bin/activate
   pip install -r requirements.txt  # currently empty, but handy for future dependencies
   ```

2. **Run the CLI from the project root:**
   ```bash
   python3 cli.py <command> [args]
   ```

3. If you launch without any arguments, it will prompt you:
   ```text
   $ python3 cli.py
   Enter command: add Buy milk
   Task added successfully: 1
   ```


## Commands

| Command                         | What it does                                | Example                              |
|---------------------------------|---------------------------------------------|--------------------------------------|
| `add <description>`             | create a new task                           | `add Write report`                   |
| `update <id> <new description>` | change the text of an existing task        | `update 2 Rewrite section`           |
| `delete <id>`                   | remove a task by its ID                     | `delete 5`                           |
| `mark-in-progress <id>`         | set status to **in-progress**               | `mark-in-progress 3`                 |
| `mark-done <id>`                | set status to **done**                      | `mark-done 3`                        |
| `list [status]`                 | show all tasks, optionally filtered by status | `list` or `list todo`              |

Valid statuses are `todo`, `in-progress`, and `done`.
