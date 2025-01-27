import os
import pytest
from dotenv import load_dotenv
from model.user import User, UserCreate, UserUpdate
from error import MissingUser, DuplicateUser

# Set environment variable for in-memory database
load_dotenv()
os.environ["TODO_SQLITE_DB"] = ":memory:"
from data import user


# FIXTURES
@pytest.fixture(autouse=True)
def clear_database() -> None:
    """Automatically clear the database before each test."""
    user.delete_all_users()


@pytest.fixture
def new_user() -> UserCreate:
    """Provide a new user for testing."""
    return UserCreate(name="test user", hash="test hash")


@pytest.fixture
def created_user(new_user: UserCreate) -> User:
    """Create and return a user for testing."""
    return user.create_user(new_user)


@pytest.fixture
def modified_user() -> UserCreate:
    """Provide a modified user for testing."""
    return UserUpdate(name="modified user", hash="modified hash")


# TESTS
def test_create_user(new_user: UserCreate) -> None:
    """Test creating a new user."""
    resp = user.create_user(new_user)
    assert hasattr(resp, "user_id")
    assert resp.name == new_user.name
    assert resp.hash == new_user.hash


def test_create_user_duplicate(new_user: UserCreate) -> None:
    """Test creating a duplicate user raises a Duplicate exception."""
    user.create_user(new_user)
    with pytest.raises(DuplicateUser):
        user.create_user(new_user)


def test_get_single_user(created_user: User) -> None:
    """Test retrieving a single user by ID."""
    resp = user.get_single_user(created_user.user_id)
    assert resp == created_user


def test_get_single_user_missing() -> None:
    """Verify that attempting to retrieve a non-existent user raises a MissingUser exception."""
    with pytest.raises(MissingUser):
        user.get_single_user(-1)


def test_get_all_users(created_user: User) -> None:
    """Ensure all users can be retrieved when at least one user exists."""
    resp = user.get_all_users()
    assert resp == [created_user]


def test_get_all_users_empty() -> None:
    """Ensure an empty list is returned when no users exist."""
    resp = user.get_all_users()
    assert resp == []


def test_modify(created_user: User, modified_user: UserCreate) -> None:
    """Ensure a user can be modified successfully."""
    resp = user.modify_user(created_user.user_id, modified_user)
    assert resp.name == modified_user.name
    assert resp.hash == modified_user.hash


def test_modify_missing(modified_user: UserCreate) -> None:
    """Verify that modifying a non-existent user raises a MissingUser exception."""
    with pytest.raises(MissingUser):
        user.modify_user(-1, modified_user)


def test_delete(created_user: User) -> None:
    """Ensure a user can be deleted successfully."""
    resp = user.delete_user(created_user.user_id)
    assert resp is None


def test_delete_missing() -> None:
    """Verify that attempting to delete a non-existent user raises a MissingUser exception."""
    with pytest.raises(MissingUser):
        user.delete_user(-1)


def test_delete_all_users(created_user: User) -> None:
    """Ensure all users can be deleted when at least one user exists."""
    assert user.get_all_users() == [created_user]
    resp = user.delete_all_users()
    assert resp is None
    assert user.get_all_users() == []


def test_delete_all_users_empty() -> None:
    """Ensure no errors occur when deleting users from an empty database."""
    assert user.get_all_users() == []
    resp = user.delete_all_users()
    assert resp is None
    assert user.get_all_users() == []
