import os
import pytest
from dotenv import load_dotenv
from model.task import Task, TaskCreate
from error import DuplicateTask, MissingTask

load_dotenv()
os.environ["TODO_UNIT_TEST"] = "true"

from service import task


# FIXTURES
@pytest.fixture(autouse=True)
def clear_database() -> None:
    """Automatically clear the database before each test function."""
    task.delete_all_tasks()


@pytest.fixture
def new_task() -> TaskCreate:
    """Provide a new task object for testing."""
    return TaskCreate(task="test task")


@pytest.fixture
def created_task(new_task: TaskCreate) -> Task:
    """Create and return a task in the database for testing."""
    resp: Task = task.create_task(new_task)
    return resp


@pytest.fixture
def modified_task() -> TaskCreate:
    """Provide a modified task object for testing."""
    return TaskCreate(task="modified task")


# TESTS
def test_create_task(new_task: TaskCreate) -> None:
    resp = task.create_task(new_task)
    assert hasattr(resp, "task_id")
    assert resp.task == new_task.task


def test_create_task_duplicate(new_task: TaskCreate) -> None:
    task.create_task(new_task)
    with pytest.raises(DuplicateTask):
        task.create_task(new_task)


def test_get_single_task(created_task: Task) -> None:
    resp = task.get_single_task(created_task.task_id)
    assert resp == created_task


def test_get_single_task_missing() -> None:
    with pytest.raises(MissingTask):
        task.get_single_task(-1)


def test_get_all_tasks(created_task: Task) -> None:
    """Test retrieving all tasks when there is at least one task."""
    resp: list[Task] = task.get_all_tasks()
    assert resp == [created_task]


def test_get_all_tasks_empty() -> None:
    """Test retrieving all tasks when there are no tasks."""
    resp: list[Task] = task.get_all_tasks()
    assert resp == []


def test_modify_task(created_task: Task, modified_task: TaskCreate) -> None:
    resp = task.modify_task(created_task.task_id, modified_task)
    assert resp.task == modified_task.task


def test_modify_task_missing(modified_task: TaskCreate) -> None:
    with pytest.raises(MissingTask):
        task.modify_task(-1, modified_task)


def test_delete_task(created_task: Task) -> None:
    resp = task.delete_task(created_task.task_id)
    assert resp is None


def test_delete_task_missing() -> None:
    with pytest.raises(MissingTask):
        task.delete_task(-1)


def test_delete_all_tasks(created_task: Task) -> None:
    """Test deleting all tasks when there is at least one task."""
    assert task.get_all_tasks() == [created_task]
    task.delete_all_tasks()
    assert task.get_all_tasks() == []


def test_delete_all_tasks_empty() -> None:
    """Test deleting all tasks when there are no tasks."""
    assert task.get_all_tasks() == []
    task.delete_all_tasks()
    assert task.get_all_tasks() == []
