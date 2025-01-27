from model.task import Task, TaskCreate
from error import Missing, Duplicate

_tasks: list[Task] = []


def find(task_id: int) -> Task | None:
    for t in _tasks:
        if t.task_id == task_id:
            return t
    return None


def check_duplicate(current_task: Task, modified_task: TaskCreate) -> None:
    if current_task.task == modified_task.task:
        raise Duplicate(modified_task)


def check_missing(task_id: int) -> None:
    if not find(task_id):
        raise Missing(task_id)


def get_all_tasks() -> list[Task]:
    """Return all tasks in database"""
    return _tasks


def get_single_task(task_id: int) -> Task:
    """Return a single task in the database if it exists"""
    check_missing(task_id)
    return find(task_id)


def create_task(task: TaskCreate) -> Task:
    """Add a new task to the database"""
    # Determine the next available task_id
    next_task_id = max(t.task_id for t in _tasks) + 1 if _tasks else 1
    new_task = Task(task_id=next_task_id, task=task.task)

    # Check for duplicates
    for t in _tasks:
        check_duplicate(t, new_task)

    _tasks.append(new_task)
    return new_task


def modify_task(task_id: int, modified_task: TaskCreate) -> Task:
    """Modify a task in the database"""
    check_missing(task_id)
    task = find(task_id)
    check_duplicate(task, modified_task)
    task.task = modified_task.task
    return task


def delete_task(task_id: int) -> None:
    """Delete a task from the database"""
    check_missing(task_id)
    task = find(task_id)
    _tasks.remove(task)


def delete_all_tasks() -> None:
    """Delete all tasks from the database"""
    _tasks.clear()
