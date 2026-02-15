import sys
import json
import os
import datetime

FILE_NAME = "tasks.json"


def load_tasks():
    if not os.path.exists(FILE_NAME):
        return []
    
    with open(FILE_NAME, "r") as file:
        data = json.load(file)
        return [Task.from_dict(item) for item in data]



def save_tasks(tasks):
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
    
    def to_dict(self):
        """Put data to dict"""
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
