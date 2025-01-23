from random import randint
from model.task import Task, TaskCreate

_tasks = [
    Task(task_id=1, task="Make grocery list"),
    Task(task_id=2, task="Close bank account"),
    Task(task_id=3, task="Call plumber"),
    Task(task_id=4, task="Meet with consultant"),
    Task(task_id=5, task="Review monthly expenses")
]


def get_all_tasks() -> list[Task]:
    """Return all tasks in database"""
    return _tasks


def get_single_task(task_id: int) -> Task | None:
    """Return a single task in the database if it exists"""
    for task in _tasks:
        if task.task_id == task_id:
            return task
    return None


def create_task(task: TaskCreate) -> Task:
    """Add a new task to the database"""
    new_task = Task(task_id=randint(100, 1000), task=task.task)
    _tasks.append(new_task)
    return new_task


def modify_task(task_id: int, updated_task: TaskCreate) -> Task | None:
    """Modify a task in the database"""
    task = get_single_task(task_id)
    if task:
        task.task = updated_task.task
    return task


def delete_task(task_id: int) -> Task | bool:
    """Delete a task from the database"""
    task = get_single_task(task_id)
    if task:
        _tasks.remove(task)
        return task
    return False