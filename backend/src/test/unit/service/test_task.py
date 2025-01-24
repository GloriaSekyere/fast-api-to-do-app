import os
import pytest
from dotenv import load_dotenv
from model.task import Task, TaskCreate
from error import Duplicate, Missing
from service import task

load_dotenv()
os.environ["TODO_UNIT_TEST"] = "true"


@pytest.fixture
def sample_new_task() -> TaskCreate:
    return TaskCreate(task="test task")


@pytest.fixture
def sample_single_task() -> Task:
    return Task(task_id=6, task="test task")


@pytest.fixture
def sample_all_tasks() -> list[Task]:
    return task.get_all_tasks()


def test_create_task(sample_new_task, sample_single_task):
    assert task.create_task(sample_new_task) == sample_single_task


def test_create_task_duplicate(sample_new_task):
    with pytest.raises(Duplicate):
        task.create_task(sample_new_task)


def test_get_single_task(sample_single_task):
    assert task.get_single_task(sample_single_task.task_id) == sample_single_task


def test_get_single_task_missing():
    with pytest.raises(Missing):
        task.get_single_task(10)


def test_modify_task(sample_single_task):
    assert (
        task.modify_task(sample_single_task.task_id, sample_single_task)
        == sample_single_task
    )


def test_modify_task_missing():
    with pytest.raises(Missing):
        thing = Task(task_id=10, task="task that does not exist")
        task.modify_task(thing.task_id, thing)


def test_delete_task(sample_single_task):
    assert task.delete_task(sample_single_task.task_id) is None


def test_delete_task_missing():
    with pytest.raises(Missing):
        task.delete_task(999)


def test_delete_all_tasks():
    assert task.delete_all_tasks() is None


def test_delete_all_tasks_missing():
    with pytest.raises(Missing):
        task.delete_all_tasks()
