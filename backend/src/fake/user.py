from model.user import User, UserCreate, UserUpdate
from error import MissingUser, DuplicateUser


_users = [
    User(user_id=1, name="kakra", hash="abc"),
    User(user_id=2, name="twyla ", hash="xyz"),
]


def find(user_id: int) -> User | None:
    for user in _users:
        if user.user_id == user_id:
            return user
    return None


def check_missing(user_id: int):
    if not find(user_id):
        raise MissingUser(user_id)


def check_duplicate(user: UserCreate | UserUpdate):
    for u in _users:
        if u.name == user.name:
            raise DuplicateUser(user)


def get_all_users() -> list[User]:
    """Return all users"""
    return _users


def get_single_user(user_id: int) -> User:
    """Return one user"""
    check_missing(user_id)
    return find(user_id)


def create_user(user: UserCreate) -> User:
    """Add a user"""
    check_duplicate(user)
    new_user = User(user_id=len(_users) + 1, name=user.name, hash=user.hash)
    _users.append(new_user)
    return new_user


def modify_user(user_id: int, user: UserUpdate) -> User:
    """Partially modify a user"""
    check_missing(user_id)
    user_to_modify = find(user_id)

    if user.name and user.name != user_to_modify.name:
        check_duplicate(user)
        user_to_modify.name = user.name

    if user.hash:
        user_to_modify.hash = user.hash

    return user_to_modify


def delete_user(user_id: int) -> None:
    """Delete a user"""
    check_missing(user_id)
    _users.remove(find(user_id))


def delete_all_users() -> None:
    """Delete all users"""
    _users.clear()
