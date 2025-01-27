import os
import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from model.task import Task, TaskCreate
from main import app

# Load environment variables from .env file
load_dotenv()

# Use an in-memory SQLite database for testing
os.environ["TODO_SQLITE_DB"] = ":memory:"

# Create a test client for the FastAPI app
client = TestClient(app)

missing_msg = 'Task with id "-1" not found'


# FIXTURES
@pytest.fixture(scope="function")
def clear_database() -> None:
    """Fixture to clear the database before each test function."""
    client.delete("/task")


@pytest.fixture(scope="session")
def new_task() -> TaskCreate:
    """Fixture to provide a new task for testing."""
    return TaskCreate(task="test task")


@pytest.fixture(scope="function")
def created_task() -> Task:
    """Fixture to create a task in the database for testing."""
    new_task = TaskCreate(task="created task")
    resp = client.post("/task", json=new_task.model_dump())
    assert resp.status_code == 201
    return Task(**resp.json())


@pytest.fixture(scope="function")
def modified_task() -> TaskCreate:
    """Fixture to provide a modified task for testing."""
    return TaskCreate(task="modified task")


# TESTS
def test_create_task(new_task: TaskCreate) -> None:
    """Test creating a new task."""
    resp = client.post("/task", json=new_task.model_dump())
    assert resp.status_code == 201


def test_create_task_duplicate(new_task: TaskCreate) -> None:
    """Test creating a duplicate task."""
    resp = client.post("/task", json=new_task.model_dump())
    assert resp.status_code == 409


def test_get_single_task(created_task: Task) -> None:
    """Test retrieving a single task by ID."""
    resp = client.get(f"/task/{created_task.task_id}")
    assert resp.status_code == 200
    assert resp.json() == created_task.model_dump()


def test_get_single_task_missing() -> None:
    """Test retrieving a task that does not exist."""
    resp = client.get("/task/-1")
    assert resp.status_code == 404
    assert resp.json().get("detail") == missing_msg


def test_get_all_tasks(clear_database, created_task: Task) -> None:
    """Test retrieving all tasks when there is one task."""
    resp = client.get("/task")
    assert resp.status_code == 200
    assert resp.json() == [created_task.model_dump()]


def test_get_all_tasks_empty(clear_database) -> None:
    """Test retrieving all tasks when there are no tasks."""
    resp = client.get("/task")
    assert resp.status_code == 200
    assert resp.json() == []


def test_modify_task(created_task: Task, modified_task: TaskCreate) -> None:
    """Test modifying an existing task."""
    resp = client.patch(
        f"/task/{created_task.task_id}", json=modified_task.model_dump()
    )
    assert resp.status_code == 200
    assert resp.json().get("task") == modified_task.task


def test_modify_task_missing(modified_task: TaskCreate) -> None:
    """Test modifying a task that does not exist."""
    resp = client.patch("/task/-1", json=modified_task.model_dump())
    assert resp.status_code == 404
    assert resp.json().get("detail") == missing_msg


def test_delete_task(created_task: Task) -> None:
    """Test deleting an existing task."""
    resp = client.delete(f"/task/{created_task.task_id}")
    assert resp.status_code == 204


def test_delete_task_missing() -> None:
    """Test deleting a task that does not exist."""
    resp = client.delete("/task/-1")
    assert resp.status_code == 404
    assert resp.json().get("detail") == missing_msg


def test_delete_all_tasks(clear_database, created_task: Task) -> None:
    """Test deleting all tasks."""
    resp = client.delete("/task")
    assert resp.status_code == 204


def test_delete_all_tasks_empty(clear_database) -> None:
    """Test deleting all tasks when there are no tasks."""
    resp = client.delete("/task")
    assert resp.status_code == 204
