# Data exceptions
from model.task import TaskCreate
from model.user import UserCreate


# Task exceptions
class DuplicateTask(Exception):
    def __init__(self, task: TaskCreate):
        self.msg = f'Task "{task.task}" already exists'


class MissingTask(Exception):
    def __init__(self, task_id: int):
        self.msg = f'Task with id "{task_id}" not found'


# User exceptions
class DuplicateUser(Exception):
    def __init__(self, user: UserCreate):
        self.msg = f'User "{user.name}" already exists'


class MissingUser(Exception):
    def __init__(self, user_id: int | None = None, name: str | None = None):
        if user_id:
            self.msg = f'User with id "{user_id}" not found'
        elif name:
            self.msg = f'User with name "{name}" not found'
        else:
            self.msg = "User not found"
