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
    :rtype: str
    """

    def is_arguments(args: list) -> bool:
        """
        Checks arguments existing (if needs)
        
        :param args: cli command
        :type args: list
        :return: True if exists, False if not
        :rtype: bool
        """

        if len(args) < 3:
            return False
        return True

    args = sys.argv

    if len(args) < 2: # Command existing check
        print("No command provided")
        return
    
    command = args[1]
    if command == "add":
        if not is_arguments(args):
            return
        return {"command": command, "description": args[-1]}
    elif command == "update":
        if not is_arguments(args):
            return
        description = " ".join(args[2:])
        return {"command": command, "new_description": args[-1]}
    elif command == "delete":
        if not is_arguments(args):
            return
        return {"command": command, "id": args[-1]}
    elif command == "list":
        if is_arguments(args):
            argument = args[2] if len(args) > 2 else None
            return {"command": command, "argument": argument}
        return {"command": command}


def load_tasks() -> list:
    """
    Loading tasks and putting them into list of objects.
    
    :return: list of Task objects
    :rtype: list
    """

    if not os.path.exists(FILE_NAME):
        return []
    
    with open(FILE_NAME, "r") as file:
        data = json.load(file)
        return [Task.from_dict(item) for item in data]


def save_tasks(tasks: list) -> None:
    """
    Puts tasks into list of dicts and pushes it to the FILE_NAME
    
    :param tasks: list of Task objects
    :type tasks: list
    """
    items = [item.to_dict() for item in tasks]
    with open(FILE_NAME, "w") as file:
        json.dump(items, file, indent=4)


class Task:
    def __init__(self, id, description, status="todo", created_at=None, updated_at=None):
        self.id = id
        self.description = description
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at
    
    def to_dict(self) -> dict:
        """
        Puts values into dictionary
        
        :param self: objects
        """
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
            status=data["status"],
            created_at=data["created_at"],
            updated_at=data["updated_at"]
        )


def main():
    tasks = [Task(1, "Test", "todo", str(datetime.datetime.now()), str(datetime.datetime.now()))]

    save_tasks(tasks)
    svo = load_tasks()
    print(svo)

if __name__ == "__main__":
    main()
