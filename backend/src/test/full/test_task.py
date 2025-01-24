import pytest
from fastapi.testclient import TestClient
from model.task import Task, TaskCreate
from main import app


client = TestClient(app)


@pytest.fixture(scope="session")
def sample_new_task() -> TaskCreate:
    return TaskCreate(task="test task")


@pytest.fixture(scope="session")
def created_task(sample_new_task) -> dict:
    resp = client.post("/task", json=sample_new_task.model_dump())
    assert resp.status_code == 201
    task = resp.json()
    return {"task_id": task.get("task_id"), "task": task.get("task")}


@pytest.fixture(scope="session")
def sample_single_task() -> Task:
    return Task(task_id=0, task="single test task")


def test_get_single_task(created_task):
    resp = client.get(f"/task/{created_task.get('task_id')}")
    assert resp.status_code == 200
    assert resp.json() == created_task


def test_get_single_task_missing():
    resp = client.get("/task/10")
    assert resp.status_code == 404


def test_modify_task(created_task):
    modified_task = TaskCreate(task="modified test task")
    resp = client.patch(f"/task/{created_task.get('task_id')}", json=modified_task.model_dump())
    assert resp.status_code == 200
    assert resp.json().get("task") == modified_task.task


def test_modify_task_missing():
    resp = client.patch("/task/10", json={"task": "test missing task"})
    assert resp.status_code == 404


def test_delete_task(created_task):
    resp = client.delete(f"/task/{created_task.get('task_id')}")
    assert resp.status_code == 204


def test_delete_task_missing():
    resp = client.delete("/task/10")
    assert resp.status_code == 404
