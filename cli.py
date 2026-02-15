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

    if len(args) < 2:  # Command existing check
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
            print("Arguments required for update")
            return {"command": None}
        new_description = " ".join(args[2:])
        return {"command": command, "new_description": new_description}
    elif command == "delete":
        if not is_arguments(args):
            print("ID required for delete")
            return {"command": None}
        return {"command": command, "id": args[2]}
    elif command == "list":
        argument = args[2] if len(args) > 2 else None
        return {"command": command, "argument": argument}
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


def add_task(description) -> None:
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
    command = command_handler()
    if command["command"] is None:
        exit()

    if command["command"] == "add":
        add_task(command["description"])
        print("Task added successfully.")


if __name__ == "__main__":
    main()
