import json
from datetime import datetime

class Task: 
    _id_counter = 0

    def __init__(self, description) -> None:
        Task._id_counter += 1

        self.id = Task._id_counter
        self.description = description
        self.status = 'todo'
        self.createdAt = datetime.now()
        self.updatedAt = datetime.now()
    
    def add(self, filename):
        data = {
            'id': self.id,
            'description': self.description,
            'status': self.status,
            'createdAt': self.createdAt.strftime('%Y-%m-%d %H:%M:%S'),
            'updatedAt': self.updatedAt.strftime('%Y-%m-%d %H:%M:%S'),
        }

        try:
            with open(filename, 'r', encoding='utf-8') as file:
                try:
                    tasks = json.load(file)
                except json.JSONDecodeError:
                    # Если JSON поврежден или пуст, начинаем с пустого списка
                    tasks = []
        except FileNotFoundError:
            tasks = []
        
        tasks.append(data)
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(tasks, file, indent=4, ensure_ascii=False)

test = Task('test')
test.add('tasks.json')
