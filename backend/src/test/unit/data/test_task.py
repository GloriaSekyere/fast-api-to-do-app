import os
import pytest
from dotenv import load_dotenv
from model.task import Task, TaskCreate
from error import Missing, Duplicate

# set this before data imports below for data.init
load_dotenv()
os.environ["TODO_SQLITE_DB"] = ":memory:"
from data import task


@pytest.fixture
def sample_new_task() -> TaskCreate:
    return TaskCreate(task="test task")


@pytest.fixture
def created_task(sample_new_task) -> Task:
    resp = task.create_task(sample_new_task)
    return resp


@pytest.fixture
def sample_modified_task() -> TaskCreate:
    return TaskCreate(task="modified task")


@pytest.fixture
def sample_all_tasks() -> list[Task]:
    return task.get_all_tasks()


def test_create_task(sample_new_task):
    resp = task.create_task(sample_new_task)
    assert hasattr(resp, "task_id")
    assert resp.task == sample_new_task.task


def test_get_one(created_task):
    resp = task.get_single_task(created_task.task_id)
    assert resp == created_task


def test_get_one_missing():
    with pytest.raises(Missing):
        _ = task.get_single_task(10)


def test_modify(created_task, sample_modified_task):
    resp = task.modify_task(created_task.task_id, sample_modified_task)
    assert resp.task == sample_modified_task.task


def test_modify_missing(sample_modified_task):
    with pytest.raises(Missing):
        _ = task.modify_task(10, sample_modified_task)


def test_delete(created_task):
    resp = task.delete_task(created_task.task_id)
    assert resp is None


def test_delete_missing():
    with pytest.raises(Missing):
        _ = task.delete_task(10)
