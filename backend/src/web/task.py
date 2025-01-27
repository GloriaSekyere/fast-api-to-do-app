import os
from fastapi import APIRouter, HTTPException
from dotenv import load_dotenv
from error import MissingTask, DuplicateTask
from model.task import Task, TaskCreate

load_dotenv()

if os.getenv("TODO_UNIT_TEST"):
    from fake import task as service
else:
    from service import task as service


router = APIRouter(prefix="/task")


@router.get("/{task_id}")
def get_single_task(task_id: int) -> Task:
    """Return a single task if it exists"""
    try:
        return service.get_single_task(task_id)
    except MissingTask as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.get("")
@router.get("/")
def get_all_tasks() -> list[Task]:
    """Return list of all tasks"""
    try:
        return service.get_all_tasks()
    except MissingTask as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.post("", status_code=201)
@router.post("/", status_code=201)
def create_task(task: TaskCreate) -> Task:
    """Add a new task to the database"""
    try:
        return service.create_task(task)
    except DuplicateTask as exc:
        raise HTTPException(status_code=409, detail=exc.msg)


@router.patch("/{task_id}", status_code=200)
def modify_task(task_id: int, modified_task: TaskCreate) -> Task:
    """Modify a task if it exists"""
    try:
        return service.modify_task(task_id, modified_task)
    except MissingTask as exc:
        raise HTTPException(status_code=404, detail=exc.msg)
    except DuplicateTask as exc:
        raise HTTPException(status_code=409, detail=exc.msg)


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int) -> None:
    """Delete a task from the database if it exists"""
    try:
        service.delete_task(task_id)
    except MissingTask as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.delete("", status_code=204)
@router.delete("/", status_code=204)
def delete_all_tasks() -> None:
    """Delete all tasks from the database"""
    service.delete_all_tasks()
