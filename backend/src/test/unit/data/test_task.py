import os
import pytest
from dotenv import load_dotenv
from model.task import Task, TaskCreate
from error import MissingTask, DuplicateTask

# Set environment variable for in-memory database
load_dotenv()
os.environ["TODO_SQLITE_DB"] = ":memory:"
from data import task


# FIXTURES
@pytest.fixture(autouse=True)
def clear_database() -> None:
    """Automatically clear the database before each test."""
    task.delete_all_tasks()


@pytest.fixture
def new_task() -> TaskCreate:
    """Provide a new task for testing."""
    return TaskCreate(task="test task")


@pytest.fixture
def created_task(new_task: TaskCreate) -> Task:
    """Create and return a task for testing."""
    return task.create_task(new_task)


@pytest.fixture
def modified_task() -> TaskCreate:
    """Provide a modified task for testing."""
    return TaskCreate(task="modified task")


# TESTS
def test_create_task(new_task: TaskCreate) -> None:
    """Test creating a new task."""
    resp = task.create_task(new_task)
    assert hasattr(resp, "task_id")
    assert resp.task == new_task.task


def test_create_task_duplicate(new_task: TaskCreate) -> None:
    """Test creating a duplicate task raises a Duplicate exception."""
    task.create_task(new_task)
    with pytest.raises(DuplicateTask):
        task.create_task(new_task)


def test_get_single_task(created_task: Task) -> None:
    """Test retrieving a single task by ID."""
    resp = task.get_single_task(created_task.task_id)
    assert resp == created_task


def test_get_single_task_missing() -> None:
    """Test retrieving a non-existent task raises a Missing exception."""
    with pytest.raises(MissingTask):
        task.get_single_task(-1)


def test_get_all_tasks(created_task: Task) -> None:
    """Test retrieving all tasks when tasks exist."""
    resp = task.get_all_tasks()
    assert resp == [created_task]


def test_get_all_tasks_empty() -> None:
    """Test retrieving all tasks when no tasks exist."""
    resp = task.get_all_tasks()
    assert resp == []


def test_modify(created_task: Task, modified_task: TaskCreate) -> None:
    """Test modifying an existing task."""
    resp = task.modify_task(created_task.task_id, modified_task)
    assert resp.task == modified_task.task


def test_modify_missing(modified_task: TaskCreate) -> None:
    """Test modifying a non-existent task raises a Missing exception."""
    with pytest.raises(MissingTask):
        task.modify_task(-1, modified_task)


def test_delete(created_task: Task) -> None:
    """Test deleting an existing task."""
    resp = task.delete_task(created_task.task_id)
    assert resp is None


def test_delete_missing() -> None:
    """Test deleting a non-existent task raises a Missing exception."""
    with pytest.raises(MissingTask):
        task.delete_task(-1)


def test_delete_all_tasks(created_task: Task) -> None:
    """Test deleting all tasks when tasks exist."""
    assert task.get_all_tasks() == [created_task]
    resp = task.delete_all_tasks()
    assert resp is None
    assert task.get_all_tasks() == []


def test_delete_all_tasks_empty() -> None:
    """Test deleting all tasks when no tasks exist."""
    assert task.get_all_tasks() == []
    resp = task.delete_all_tasks()
    assert resp is None
    assert task.get_all_tasks() == []
