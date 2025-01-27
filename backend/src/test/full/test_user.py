import os
import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from model.user import User, UserCreate
from main import app

# Load environment variables from .env file
load_dotenv()

# Use an in-memory SQLite database for testing
os.environ["TODO_SQLITE_DB"] = ":memory:"

# Create a test client for the FastAPI app
client = TestClient(app)

missing_msg = 'User with id "-1" not found'


# FIXTURES
@pytest.fixture(scope="function")
def clear_database() -> None:
    """Fixture to clear the database before each test function."""
    client.delete("/user")


@pytest.fixture(scope="session")
def new_user() -> UserCreate:
    """Fixture to provide a new user for testing."""
    return UserCreate(name="test user", hash="test hash")


@pytest.fixture(scope="function")
def created_user() -> User:
    """Fixture to create a user in the database for testing."""
    new_user = UserCreate(name="created user", hash="created hash")
    resp = client.post("/user", json=new_user.model_dump())
    assert resp.status_code == 201
    return User(**resp.json())


@pytest.fixture(scope="function")
def modified_user() -> UserCreate:
    """Fixture to provide a modified user for testing."""
    return UserCreate(name="modified user", hash="modified hash")


# TESTS
def test_create_user(new_user: UserCreate) -> None:
    """Test creating a new user."""
    resp = client.post("/user", json=new_user.model_dump())
    assert resp.status_code == 201


def test_create_user_duplicate(new_user: UserCreate) -> None:
    """Test creating a duplicate user."""
    resp = client.post("/user", json=new_user.model_dump())
    assert resp.status_code == 409


def test_get_single_user(created_user: User) -> None:
    """Test retrieving a single user by ID."""
    resp = client.get(f"/user/{created_user.user_id}")
    assert resp.status_code == 200
    assert resp.json() == created_user.model_dump()


def test_get_single_user_missing() -> None:
    """Test retrieving a user that does not exist."""
    resp = client.get("/user/-1")
    assert resp.status_code == 404
    assert resp.json().get("detail") == missing_msg


def test_get_all_users(clear_database, created_user: User) -> None:
    """Test retrieving all users when there is one user."""
    resp = client.get("/user")
    assert resp.status_code == 200
    assert resp.json() == [created_user.model_dump()]


def test_get_all_users_empty(clear_database) -> None:
    """Test retrieving all users when there are no users."""
    resp = client.get("/user")
    assert resp.status_code == 200
    assert resp.json() == []


def test_modify_user(created_user: User, modified_user: UserCreate) -> None:
    """Test modifying an existing user."""
    resp = client.patch(
        f"/user/{created_user.user_id}", json=modified_user.model_dump()
    )
    assert resp.status_code == 200
    assert resp.json().get("name") == modified_user.name


def test_modify_user_missing(modified_user: UserCreate) -> None:
    """Test modifying a user that does not exist."""
    resp = client.patch("/user/-1", json=modified_user.model_dump())
    assert resp.status_code == 404
    assert resp.json().get("detail") == missing_msg


def test_delete_user(created_user: User) -> None:
    """Test deleting an existing user."""
    resp = client.delete(f"/user/{created_user.user_id}")
    assert resp.status_code == 204


def test_delete_user_missing() -> None:
    """Test deleting a user that does not exist."""
    resp = client.delete("/user/-1")
    assert resp.status_code == 404
    assert resp.json().get("detail") == missing_msg


def test_delete_all_users(clear_database, created_user: User) -> None:
    """Test deleting all users."""
    resp = client.delete("/user")
    assert resp.status_code == 204


def test_delete_all_users_empty(clear_database) -> None:
    """Test deleting all users when there are no users."""
    resp = client.delete("/user")
    assert resp.status_code == 204
