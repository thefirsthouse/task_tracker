import sys
import json
import os
import datetime

FILE_NAME = "tasks.json"


def command_handler() -> dict:
    """
    CLI command handler.
    Gets commands, validates, and returns clear request.
    
    :return: Clear request and arguments (if exists)
    :rtype: dict
    """

    def is_arguments(args: list) -> bool:
        """Checks arguments existence"""
        return len(args) >= 3

    args = sys.argv

    if len(args) < 2: ## unremove after debug
        print("No command provided")
        return {"command": None}

    command = args[1]
    if command == "add":
        if not is_arguments(args):
            print("Description required")
            return {"command": None}
        description = " ".join(args[2:])
        return {"command": command, "description": description}
    elif command == "update":
        if not is_arguments(args):
            print("ID and new description required for update")
            return {"command": None}

        task_id_str = args[2]
        try:
            task_id = int(task_id_str)
        except ValueError:
            print("ID must be an integer")
            return {"command": None}

        new_description = " ".join(args[3:])

        return {"command": command, "id": task_id, "new_description": new_description}

    elif command == "delete":
        if not is_arguments(args):
            print("ID required for delete")
            return {"command": None}

        task_id_str = args[2]
        try:
            task_id = int(task_id_str)
        except ValueError:
            print("ID must be an integer")
            return {"command": None}

        return {"command": command, "id": task_id}
    
    elif command == "mark-in-progress" or command == "mark-done":
        if not is_arguments(args):
            print("Task ID is required")
            return {"command": None}
        
        task_id_str = args[2]
        try:
            task_id = int(task_id_str)
        except ValueError:
            print("ID must be an integer")
            return {"command": None}
        
        if command == "mark-in-progress":
            status = "in-progress"
        else:
            status = "done"
        
        return {"command": command, "id": task_id, "status": status}

    elif command == "list":
        if is_arguments(args):
            argument = args[2]
            if argument not in ["todo", "in-progress", "done"]:
                print("Invalid status filter. Use 'todo', 'in-progress', or 'done'.")
                return {"command": None}
            return {"command": command, "status_filter": argument}
        return {"command": command}
    
    else:
        print("Invalid command")
        return {"command": None}


def load_tasks() -> list:
    """Loading tasks and putting them into list of objects."""
    if not os.path.exists(FILE_NAME):
        return []
    
    with open(FILE_NAME, "r") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data = []
        return [Task.from_dict(item) for item in data]


def save_tasks(tasks: list) -> None:
    """Puts tasks into list of dicts and pushes it to the FILE_NAME"""
    items = [item.to_dict() for item in tasks]
    with open(FILE_NAME, "w") as file:
        json.dump(items, file, indent=4, default=str)


def add_task(description: str) -> None:
    """Creates a task"""
    tasks = load_tasks()
    new_id = max((task.id for task in tasks), default=0) + 1

    now = str(datetime.datetime.now())

    task = Task(
        id=new_id,
        description=description,
        status="todo",
        created_at=now,
        updated_at=now
    )

    tasks.append(task)
    save_tasks(tasks)


def update_task(id: int, new_description) -> bool:
    """
    Updates task by id. Returns True if a task was updated.

    :param id: Task id
    :type id: int
    :returns: whether an update occurred
    :rtype: bool
    """

    # ensure id is integer
    try:
        id = int(id)
    except (TypeError, ValueError):
        return False

    tasks = load_tasks()
    found = False
    for task in tasks:
        if task.id == id:
            task.description = new_description
            task.updated_at = str(datetime.datetime.now())
            found = True
            break

    if found:
        save_tasks(tasks)
        print(f"Task {id} updated")
    else:
        print(f"Task {id} not found")
    return found


def delete_task(id: int) -> bool:
    """
    Deletes task by id. Returns True if a task was deleted.
    
    :param id: Task id
    :type id: int
    :return: whether a task was deleted
    :rtype: bool
    """

    try:
        id = int(id)
    except (TypeError, ValueError):
        return False

    tasks = load_tasks()
    for task in tasks:
        if task.id == id:
            tasks.remove(task)
            save_tasks(tasks)
            print(f"Task {id} deleted")
            return True
    
    print(f"Task {id} not found")
    return False


def mark_task(id: int, status: str) -> bool:
    """
    Edit task status
    
    :param id: Task id
    :type id: int
    :return: whether a task status was updated 
    :rtype: bool
    """

    try:
        id = int(id)
    except (TypeError, ValueError):
        return False
    
    tasks = load_tasks()
    for task in tasks:
        if task.id == id:
            task.status = status
            save_tasks(tasks)
            print(f"Task {id} marked as {status}")
            return True
    
    print(f"Task {id} not found")
    return False


def show_tasks() -> None:
    """
    Shows all existing tasks
    """

    tasks = load_tasks()
    for task in tasks:
        print(task.id, task.description, task.status)
    
    print("=== END ===")


class Task:
    def __init__(self, id, description, status="todo", created_at=None, updated_at=None):
        self.id = id
        self.description = description
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
    
    def to_dict(self) -> dict:
        """Puts values into dictionary"""
        return {
            "id": self.id,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Get data from dict"""
        return cls(
            id=data["id"],
            description=data["description"],
            status=data.get("status", "todo"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at")
        )


def main():
    # DEBUG MODE
    if len(sys.argv) == 1:
        raw = input("Enter command: ")
        sys.argv = ["cli.py"] + raw.split()

    command = command_handler()
    # if handler returned no valid command, stop execution
    if not command.get("command"):
        return

    if command["command"] == "add":
        add_task(command["description"])
        print("Task added successfully")
    
    if command["command"] == "update":
        success = update_task(command["id"], command["new_description"])
        if success:
            print(f"Task {command['id']} updated successfully")
        else:
            print("Update failed")
    
    if command["command"] == "delete":
        success = delete_task(command["id"])
        if success:
            print(f"Task {command["id"]} has been deleted")
        else:
            print("Delete failed")
    
    if command["command"] == "mark-in-progress" or command["command"] == "mark-done":
        success = mark_task(command["id"], command["status"])
        if success:
            pass
        else:
            print("Delete failed")
    
    if command["command"] == "list" and not command.get("status_filter"):
        show_tasks()
    elif command["command"] == "list" and command.get("status_filter"):
        tasks = load_tasks()
        filtered_tasks = [task for task in tasks if task.status == command["status_filter"]]
        for task in filtered_tasks:
            print(task.id, task.description, task.status)
        print("=== END ===")
    



if __name__ == "__main__":
    main()
