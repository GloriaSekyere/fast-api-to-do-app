from data import task as data
from model.task import Task, TaskCreate


def get_all_tasks() -> list[Task]:
    """Return list of all tasks"""
    return data.get_all_tasks()


def get_single_task(task_id: int) -> Task:
    """Return a single task if it exists"""
    return data.get_single_task(task_id)


def create_task(task: TaskCreate) -> Task:
    """Add a new task"""
    return data.create_task(task)


def modify_task(task_id: int, updated_task: TaskCreate) -> Task:
    """Modify a task if it exists"""
    return data.modify_task(task_id, updated_task)


def delete_task(task_id: int) -> None:
    """Delete a task if it exsits"""
    data.delete_task(task_id)


def delete_all_tasks() -> None:
    """Delete all tasks"""
    data.delete_all_tasks()
