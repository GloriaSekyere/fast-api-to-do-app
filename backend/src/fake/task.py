from model.task import Task, TaskCreate
from error import Missing, Duplicate

_tasks = [
    Task(task_id=1, task="Make grocery list"),
    Task(task_id=2, task="Close bank account"),
    Task(task_id=3, task="Call plumber"),
    Task(task_id=4, task="Meet with consultant"),
    Task(task_id=5, task="Review monthly expenses")
]

def find(task_id: int) -> Task | None:
    for t in _tasks:
        if t.task_id == task_id:
            return t
    return None


def check_duplicate(task_id: int) -> None:
    if find(task_id):
        raise Duplicate(msg="Task already exists")


def check_missing(task_id: int) -> None:
    if not find(task_id):
        raise Missing(msg="Task not found")


def check_empty() -> None:
    if not _tasks:
        raise Missing(msg="No tasks found")


def get_all_tasks() -> list[Task]:
    """Return all tasks in database"""
    return _tasks


def get_single_task(task_id: int) -> Task:
    """Return a single task in the database if it exists"""
    check_missing(task_id)
    return find(task_id)


def create_task(task: TaskCreate) -> Task:
    """Add a new task to the database"""
    new_task = Task(task_id=6, task=task.task)
    check_duplicate(new_task.task_id)
    _tasks.append(new_task)
    return new_task


def modify_task(task_id: int, updated_task: TaskCreate) -> Task | None:
    """Modify a task in the database"""
    check_missing(task_id)
    task = find(task_id)
    if task:
        task.task = updated_task.task
    return task


def delete_task(task_id: int) -> None:
    """Delete a task from the database"""
    check_missing(task_id)
    task = find(task_id)
    if task:
        return _tasks.remove(task)


def delete_all_tasks() -> None:
    """Delete all tasks from the database"""
    check_empty()
    return _tasks.clear()
