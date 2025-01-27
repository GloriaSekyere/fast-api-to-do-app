from .init import db, IntegrityError
from model.task import Task, TaskCreate
from error import MissingTask, DuplicateTask

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
        raise MissingTask(task_id)
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
        raise DuplicateTask(task)


def modify_task(task_id: int, modified_task: TaskCreate) -> Task:
    qry = """UPDATE task
             SET task = :task
             WHERE task_id = :task_id"""
    params = model_to_dict(modified_task)
    params["task_id"] = task_id
    try:
        res = db.execute(qry, params)
        if res.rowcount == 0:
            raise MissingTask(task_id)
        return get_single_task(task_id)
    except IntegrityError:
        raise DuplicateTask(modified_task)


def delete_task(task_id: int) -> None:
    qry = "DELETE FROM task WHERE task_id = :task_id"
    params = {"task_id": task_id}
    result = db.execute(qry, params)
    if result.rowcount == 0:
        raise MissingTask(task_id)


def delete_all_tasks() -> None:
    qry = "DELETE FROM task"
    db.execute(qry)
