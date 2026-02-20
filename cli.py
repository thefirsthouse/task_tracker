import sys
import json
import os
import datetime
from dataclasses import dataclass, asdict
from typing import List, Optional

FILE_NAME = "tasks.json"
VALID_STATUSES = {"todo", "in-progress", "done"}


@dataclass
class Task:
    id: int
    description: str
    status: str = "todo"
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data["id"],
            description=data["description"],
            status=data.get("status", "todo"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )


def load_tasks() -> List[Task]:
    """Read tasks from disk and convert to Task objects."""
    if not os.path.exists(FILE_NAME):
        return []
    try:
        with open(FILE_NAME, "r") as f:
            data = json.load(f)
    except (json.JSONDecodeError, IOError):
        return []
    return [Task.from_dict(item) for item in data]


def save_tasks(tasks: List[Task]) -> None:
    """Serialize task list and write it to the JSON file."""
    with open(FILE_NAME, "w") as f:
        json.dump([task.to_dict() for task in tasks], f, indent=4, default=str)


def parse_int(value: str, name: str = "ID") -> Optional[int]:
    """Try to convert value to int, printing an error message on failure."""
    try:
        return int(value)
    except ValueError:
        print(f"{name} must be an integer")
        return None


def command_handler() -> dict:
    """Parse sys.argv and return a dict with 'command' and other args."""
    argv = sys.argv[1:]
    if not argv:
        print("No command provided")
        return {"command": None}

    cmd, *rest = argv

    if cmd == "add":
        if not rest:
            print("Description required")
            return {"command": None}
        return {"command": cmd, "description": " ".join(rest)}

    if cmd == "update":
        if not rest:
            print("ID and new description required for update")
            return {"command": None}
        task_id = parse_int(rest[0])
        if task_id is None:
            return {"command": None}
        if len(rest) < 2:
            print("New description required")
            return {"command": None}
        return {"command": cmd, "id": task_id, "new_description": " ".join(rest[1:])}

    if cmd == "delete":
        if not rest:
            print("ID required for delete")
            return {"command": None}
        task_id = parse_int(rest[0])
        if task_id is None:
            return {"command": None}
        return {"command": cmd, "id": task_id}

    if cmd in ("mark-in-progress", "mark-done"):
        if not rest:
            print("Task ID is required")
            return {"command": None}
        task_id = parse_int(rest[0])
        if task_id is None:
            return {"command": None}
        status = "in-progress" if cmd == "mark-in-progress" else "done"
        return {"command": cmd, "id": task_id, "status": status}

    if cmd == "list":
        status_filter = None
        if rest:
            if rest[0] not in VALID_STATUSES:
                print("Invalid status filter. Use 'todo', 'in-progress', or 'done'.")
                return {"command": None}
            status_filter = rest[0]
        return {"command": cmd, "status_filter": status_filter}

    print("Invalid command")
    return {"command": None}


def add_task(description: str) -> Task:
    tasks = load_tasks()
    new_id = max((t.id for t in tasks), default=0) + 1
    now = datetime.datetime.now().isoformat()
    task = Task(id=new_id, description=description, created_at=now, updated_at=now)
    tasks.append(task)
    save_tasks(tasks)
    return task


def find_task(tasks: List[Task], task_id: int) -> Optional[Task]:
    """Return the task with given id or None."""
    for t in tasks:
        if t.id == task_id:
            return t
    return None


def update_task(task_id: int, new_description: str) -> bool:
    tasks = load_tasks()
    task = find_task(tasks, task_id)
    if task:
        task.description = new_description
        task.updated_at = datetime.datetime.now().isoformat()
        save_tasks(tasks)
        return True
    print(f"Task {task_id} not found")
    return False


def delete_task(task_id: int) -> bool:
    tasks = load_tasks()
    task = find_task(tasks, task_id)
    if task:
        tasks.remove(task)
        save_tasks(tasks)
        print(f"Task {task_id} deleted")
        return True
    print(f"Task {task_id} not found")
    return False


def mark_task(task_id: int, status: str) -> bool:
    tasks = load_tasks()
    task = find_task(tasks, task_id)
    if task:
        task.status = status
        task.updated_at = datetime.datetime.now().isoformat()
        save_tasks(tasks)
        print(f"Task {task_id} marked as {status}")
        return True
    print(f"Task {task_id} not found")
    return False


def show_tasks(status_filter: Optional[str] = None) -> None:
    tasks = load_tasks()
    if status_filter:
        tasks = [t for t in tasks if t.status == status_filter]
    for t in tasks:
        print(t.id, t.description, t.status)
    print("=== END ===")


def main():
    if len(sys.argv) == 1:
        raw = input("Enter command: ")
        sys.argv += raw.split()

    command = command_handler()
    if not command.get("command"):
        return

    cmd = command["command"]
    if cmd == "add":
        task = add_task(command["description"])
        print("Task added successfully:", task.id)
    elif cmd == "update":
        if update_task(command["id"], command["new_description"]):
            print(f"Task {command['id']} updated successfully")
    elif cmd == "delete":
        delete_task(command["id"])
    elif cmd in ("mark-in-progress", "mark-done"):
        mark_task(command["id"], command["status"])
    elif cmd == "list":
        show_tasks(command.get("status_filter"))


if __name__ == "__main__":
    main()
