import datetime

statuses = ('todo', 'in progress', 'done')

class Task:
    def __init__(self, name, date, status = statuses[0]) -> None:
        self.name = name
        self.date = date
        self.status = status

# def what_to_do():
    

# def main():
    