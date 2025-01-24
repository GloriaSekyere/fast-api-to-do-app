from fastapi import HTTPException
import pytest

from dotenv import load_dotenv

load_dotenv()

import os

os.environ["TODO_UNIT_TEST"] = "true"

from model.task import Task, TaskCreate
from web import task


@pytest.fixture
def sample_new_task() -> TaskCreate:
    return TaskCreate(task="test task")


@pytest.fixture
def sample_single_task() -> Task:
    return Task(task_id=6, task="test task")


@pytest.fixture
def sample_all_tasks() -> list[Task]:
    return task.get_all_tasks()


def assert_duplicate(exc):
    assert exc.value.status_code == 409
    assert "Duplicate" in exc.value.msg


def assert_missing(exc):
    assert exc.value.status_code == 404
    assert "Missing" in exc.value.msg


def test_create_task(sample_new_task, sample_single_task):
    assert task.create_task(sample_new_task) == sample_single_task


def test_create_task_duplicate(sample_new_task):
    with pytest.raises(HTTPException) as exc:
        task.create_task(sample_new_task)
        assert_duplicate(exc)


def test_get_single_task(sample_single_task):
    assert task.get_single_task(sample_single_task.task_id) == sample_single_task


def test_get_single_task_missing():
    with pytest.raises(HTTPException) as exc:
        task.get_single_task(10)
        assert_missing(exc)


def test_modify_task(sample_single_task):
    assert (
        task.modify_task(sample_single_task.task_id, sample_single_task)
        == sample_single_task
    )


def test_modify_task_missing():
    with pytest.raises(HTTPException) as exc:
        thing = Task(task_id=10, task="task that does not exist")
        task.modify_task(thing.task_id, thing)
        assert_missing(exc)


def test_delete_task(sample_single_task):
    assert task.delete_task(sample_single_task.task_id) is None


def test_delete_task_missing(sample_single_task):
    with pytest.raises(HTTPException) as exc:
        task.delete_task(sample_single_task.task_id)
        assert_missing(exc)


def test_delete_all_tasks_missing():
    with pytest.raises(HTTPException) as exc:
        task.delete_all_tasks()
        assert_missing(exc)
