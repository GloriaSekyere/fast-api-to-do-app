import os
from model.user import User, UserCreate, UserUpdate

if os.getenv("TODO_UNIT_TEST"):
    from fake import user as data
else:
    from data import user as data


def get_all_users() -> list[User]:
    return data.get_all_users()


def get_single_user(user_id: int) -> User:
    return data.get_single_user(user_id)


def create_user(user: UserCreate) -> User:
    return data.create_user(user)


def modify_user(user_id: int, user: UserUpdate) -> User:
    return data.modify_user(user_id, user)


def delete_user(user_id: int) -> None:
    data.delete_user(user_id)


def delete_all_users() -> None:
    data.delete_all_users()
