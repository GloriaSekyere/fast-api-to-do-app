from .init import db
from model.task import Task, TaskCreate

db.execute("""CREATE TABLE IF NOT EXISTS task (
    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL)"""
)

def row_to_model(row: tuple) -> Task:
    (task_id, task) = row
    return Task(task_id=task_id, task=task)

def model_to_dict(task: Task) -> dict:
    return task.model_dump()

def get_single_task(task_id: int) -> Task:
    qry = "SELECT * FROM task WHERE task_id = :task_id"
    params = {"task_id": task_id}
    db.execute(qry, params)
    return row_to_model(db.fetchone())

def get_all_tasks() -> list[Task]:
    qry = "SELECT * FROM task"
    db.execute(qry)
    return [row_to_model(row) for row in db.fetchall()]

def create_task(task: TaskCreate) -> Task:
    qry = "INSERT INTO task (task) VALUES (:task)"
    params = model_to_dict(task)
    db.execute(qry, params)
    task_id = db.lastrowid()
    return get_single_task(task_id)

def modify_task(task_id: int, updated_task: TaskCreate) -> Task:
    qry = """UPDATE task
             SET task = :task
             WHERE task_id = :task_id"""
    params = model_to_dict(updated_task)
    params["task_id"] = task_id
    db.execute(qry, params)
    return get_single_task(task_id)

def delete_task(task_id: int) -> bool:
    qry = "DELETE FROM task WHERE task_id = :task_id"
    params = {"task_id": task_id}
    res = db.execute(qry, params)
    return res.rowcount > 0

