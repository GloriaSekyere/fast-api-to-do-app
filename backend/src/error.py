# Data exceptions
from model.task import TaskCreate


# Task exceptions
class DuplicateTask(Exception):
    def __init__(self, task: TaskCreate):
        self.msg = f'Task "{task.task}" already exists'


class MissingTask(Exception):
    def __init__(self, task_id: int):
        self.msg = f'Task with id "{task_id}" not found'
