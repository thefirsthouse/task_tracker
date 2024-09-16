import json
import datetime

statuses = frozenset('todo', 'in-progress', 'done')

class Task:
    _id_counter = 0

    def __init__(self, name, createdAt, updatedAt, status = statuses[0]) -> None:
        Task._id_counter += 1
        self.id = Task._id_counter
        self.name = name
        self.status = status
        self.createdAt = createdAt
        self.updatedAt = updatedAt
    
    def add():
        name = str(input)