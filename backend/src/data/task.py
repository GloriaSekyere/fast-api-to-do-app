from .init import db, IntegrityError
from model.task import Task, TaskCreate
from error import Missing, Duplicate

db.execute(
    """CREATE TABLE IF NOT EXISTS task (
    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL UNIQUE COLLATE NOCASE)"""
)


def row_to_model(row: tuple) -> Task:
    (task_id, task) = row
    return Task(task_id=task_id, task=task)


def model_to_dict(task: Task | TaskCreate) -> dict:
    return task.model_dump()


def get_single_task(task_id: int) -> Task:
    qry = "SELECT * FROM task WHERE task_id = :task_id"
    params = {"task_id": task_id}
    db.execute(qry, params)
    row = db.fetchone()
    if not row:
        raise Missing(f"Task with id {task_id} not found")
    return row_to_model(row)


def get_all_tasks() -> list[Task]:
    qry = "SELECT * FROM task"
    db.execute(qry)
    rows = db.fetchall()
    return [row_to_model(row) for row in rows]


def create_task(task: TaskCreate) -> Task:
    qry = "INSERT INTO task (task) VALUES (:task)"
    params = model_to_dict(task)
    try:
        db.execute(qry, params)
        task_id = db.lastrowid()
        return get_single_task(task_id)
    except IntegrityError:
        raise Duplicate(msg=f"Task {task.task} already exists")


def modify_task(task_id: int, updated_task: TaskCreate) -> Task:
    qry = """UPDATE task
             SET task = :task
             WHERE task_id = :task_id"""
    params = model_to_dict(updated_task)
    params["task_id"] = task_id
    try:
        res = db.execute(qry, params)
        if res.rowcount == 0:
            raise Missing(msg=f"Task {task_id} not found")
        return get_single_task(task_id)
    except IntegrityError:
        raise Duplicate(msg=f"Task {updated_task.task} already exists")


def delete_task(task_id: int) -> None:
    if not get_single_task(task_id):
        raise Missing(msg=f"Task {task_id} not found")
    qry = "DELETE FROM task WHERE task_id = :task_id"
    params = {"task_id": task_id}
    db.execute(qry, params)


def delete_all_tasks() -> None:
    if not get_all_tasks():
        raise Missing(msg=f"No tasks found")
    qry = "DELETE FROM task"
    db.execute(qry)
