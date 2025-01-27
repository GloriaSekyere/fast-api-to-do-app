import os
from fastapi import HTTPException
from dotenv import load_dotenv
import pytest
from model.user import User, UserCreate

load_dotenv()
os.environ["TODO_UNIT_TEST"] = "true"

from web import user


# FIXTURES
@pytest.fixture(autouse=True)
def clear_database() -> None:
    """Automatically clear the database before each test function."""
    user.delete_all_users()


@pytest.fixture
def new_user() -> UserCreate:
    """Provide a new user object for testing."""
    return UserCreate(name="test user", hash="test hash")


@pytest.fixture
def created_user(new_user: UserCreate) -> User:
    """Create and return a user in the database for testing."""
    resp: User = user.create_user(new_user)
    return resp


@pytest.fixture
def modified_user() -> UserCreate:
    """Provide a modified user object for testing."""
    return UserCreate(name="modified user", hash="modified hash")


# HELPERS
def assert_duplicate(exc: HTTPException, user: UserCreate) -> None:
    assert exc.value.status_code == 409
    assert f'User "{user.name}" already exists' in exc.value.detail


def assert_missing(exc: HTTPException, user_id: int) -> None:
    assert exc.value.status_code == 404
    assert f'User with id "{user_id}" not found' in exc.value.detail


# TESTS
def test_create_user(new_user: UserCreate) -> None:
    """Test creating a new user."""
    resp: User = user.create_user(new_user)
    assert hasattr(resp, "user_id")
    assert resp.name == new_user.name


def test_create_user_duplicate(new_user: UserCreate) -> None:
    """Test creating a duplicate user raises an HTTPException."""
    user.create_user(new_user)
    with pytest.raises(HTTPException) as exc:
        user.create_user(new_user)
    assert_duplicate(exc, new_user)


def test_get_single_user(created_user: User) -> None:
    """Test retrieving a single user by ID."""
    resp: User = user.get_single_user(created_user.user_id)
    assert resp == created_user


def test_get_single_user_missing() -> None:
    """Test retrieving a user that does not exist raises an HTTPException."""
    with pytest.raises(HTTPException) as exc:
        user.get_single_user(-1)
    assert_missing(exc, -1)


def test_get_all_users(created_user: User) -> None:
    """Test retrieving all users when there is at least one user."""
    resp: list[User] = user.get_all_users()
    assert resp == [created_user]


def test_get_all_users_empty() -> None:
    """Test retrieving all users when there are no users."""
    resp: list[User] = user.get_all_users()
    assert resp == []


def test_modify_user_name_only(created_user: User) -> None:
    """Test modifying only the user's name."""
    modified_name = "new name"
    modified_user = UserCreate(name=modified_name, hash=created_user.hash)
    resp: User = user.modify_user(created_user.user_id, modified_user)
    assert resp.name == modified_name
    assert resp.hash == created_user.hash  # Ensure hash remains unchanged


def test_modify_user_hash_only(created_user: User) -> None:
    """Test modifying only the user's hash."""
    modified_hash = "new hash"
    modified_user = UserCreate(name=created_user.name, hash=modified_hash)
    resp: User = user.modify_user(created_user.user_id, modified_user)
    assert resp.hash == modified_hash
    assert resp.name == created_user.name  # Ensure name remains unchanged


def test_modify_user_name_and_hash(created_user: User) -> None:
    """Test modifying both the user's name and hash."""
    modified_user = UserCreate(name="new name", hash="new hash")
    resp: User = user.modify_user(created_user.user_id, modified_user)
    assert resp.name == modified_user.name
    assert resp.hash == modified_user.hash


def test_modify_user_missing(modified_user: UserCreate) -> None:
    """Test modifying a user that does not exist raises an HTTPException."""
    with pytest.raises(HTTPException) as exc:
        user.modify_user(-1, modified_user)
    assert_missing(exc, -1)


def test_delete_user(created_user: User) -> None:
    """Test deleting an existing user."""
    user.delete_user(created_user.user_id)
    with pytest.raises(HTTPException) as exc:
        user.get_single_user(created_user.user_id)
    assert_missing(exc, created_user.user_id)


def test_delete_user_missing() -> None:
    """Test deleting a user that does not exist raises an HTTPException."""
    with pytest.raises(HTTPException) as exc:
        user.delete_user(-1)
    assert_missing(exc, -1)


def test_delete_all_users(created_user: User) -> None:
    """Test deleting all users when there is at least one user."""
    assert user.get_all_users() == [created_user]
    user.delete_all_users()
    assert user.get_all_users() == []


def test_delete_all_users_empty() -> None:
    """Test deleting all users when there are no users."""
    assert user.get_all_users() == []
    user.delete_all_users()
    assert user.get_all_users() == []
