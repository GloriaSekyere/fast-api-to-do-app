import os
from dotenv import load_dotenv
import pytest
from error import DuplicateUser, MissingUser
from model.user import User, UserCreate

load_dotenv()
os.environ["TODO_UNIT_TEST"] = "true"

from service import user


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


# TESTS
def test_create_user(new_user: UserCreate) -> None:
    """Ensure a new user can be created successfully."""
    resp: User = user.create_user(new_user)
    assert hasattr(resp, "user_id")
    assert resp.name == new_user.name


def test_create_user_duplicate(new_user: UserCreate) -> None:
    """Verify that creating a user with a duplicate name raises a DuplicateUser exception."""
    user.create_user(new_user)
    with pytest.raises(DuplicateUser):
        user.create_user(new_user)


def test_get_single_user(created_user: User) -> None:
    """Ensure a user can be retrieved by their ID."""
    resp: User = user.get_single_user(created_user.user_id)
    assert resp == created_user


def test_get_single_user_missing() -> None:
    """Verify that attempting to retrieve a non-existent user raises a MissingUser exception."""
    with pytest.raises(MissingUser):
        user.get_single_user(-1)


def test_get_all_users(created_user: User) -> None:
    """Ensure all users can be retrieved when at least one user exists."""
    resp: list[User] = user.get_all_users()
    assert resp == [created_user]


def test_get_all_users_empty() -> None:
    """Ensure an empty list is returned when no users exist."""
    resp: list[User] = user.get_all_users()
    assert resp == []


def test_modify_user_name_only(created_user: User) -> None:
    """Ensure a user's name can be modified without affecting their hash."""
    modified_name = "new name"
    modified_user = UserCreate(name=modified_name, hash=created_user.hash)
    resp: User = user.modify_user(created_user.user_id, modified_user)
    assert resp.name == modified_name
    assert resp.hash == created_user.hash  # Ensure hash remains unchanged


def test_modify_user_hash_only(created_user: User) -> None:
    """Ensure a user's hash can be modified without affecting their name."""
    modified_hash = "new hash"
    modified_user = UserCreate(name=created_user.name, hash=modified_hash)
    resp: User = user.modify_user(created_user.user_id, modified_user)
    assert resp.hash == modified_hash
    assert resp.name == created_user.name  # Ensure name remains unchanged


def test_modify_user_name_and_hash(created_user: User) -> None:
    """Ensure both a user's name and hash can be modified."""
    modified_user = UserCreate(name="new name", hash="new hash")
    resp: User = user.modify_user(created_user.user_id, modified_user)
    assert resp.name == modified_user.name
    assert resp.hash == modified_user.hash


def test_modify_user_missing(modified_user: UserCreate) -> None:
    """Verify that modifying a non-existent user raises a MissingUser exception."""
    with pytest.raises(MissingUser):
        user.modify_user(-1, modified_user)


def test_delete_user(created_user: User) -> None:
    """Ensure a user can be deleted and is no longer retrievable."""
    user.delete_user(created_user.user_id)
    with pytest.raises(MissingUser):
        user.get_single_user(created_user.user_id)


def test_delete_user_missing() -> None:
    """Verify that attempting to delete a non-existent user raises a MissingUser exception."""
    with pytest.raises(MissingUser):
        user.delete_user(-1)


def test_delete_all_users(created_user: User) -> None:
    """Ensure all users can be deleted when at least one user exists."""
    assert user.get_all_users() == [created_user]
    user.delete_all_users()
    assert user.get_all_users() == []


def test_delete_all_users_empty() -> None:
    """Ensure no errors occur when deleting users from an empty database."""
    assert user.get_all_users() == []
    user.delete_all_users()
    assert user.get_all_users() == []
