from fastapi import APIRouter
from service import task as service
from model.task import Task, TaskCreate

router = APIRouter(prefix="/task")


@router.get("")
@router.get("/")
def get_all_tasks() -> list[Task]:
    """Return list of all tasks"""
    return service.get_all_tasks()


@router.get("/{task_id}")
def get_single_task(task_id: int) -> Task | None:
    """Return a single task if it exists"""
    return service.get_single_task(task_id)


@router.post("", status_code=201)
@router.post("/", status_code=201)
def create_task(task: TaskCreate) -> Task:
    """Add a new task"""
    return service.create_task(task)


@router.patch("/{task_id}", status_code=200)
def modify_task(task_id: int, updated_task: TaskCreate) -> Task | None:
    """Modify a task if it exists"""
    return service.modify_task(task_id, updated_task)


@router.delete("/{task_id}")
def delete_task(task_id: int) -> Task | bool:
    """Delete a task if it exsits"""
    return service.delete_task(task_id)
