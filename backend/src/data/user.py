from model.user import User, UserCreate
from .init import db, IntegrityError
from error import MissingUser, DuplicateUser

db.execute(
    """CREATE TABLE IF NOT EXISTS user (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE COLLATE NOCASE,
            hash TEXT NOT NULL)"""
)


def row_to_model(row: tuple) -> User:
    (user_id, name, hash) = row
    return User(user_id=user_id, name=name, hash=hash)


def model_to_dict(user: User | UserCreate) -> dict:
    return user.model_dump()


def get_single_user(user_id: int) -> User:
    qry = "SELECT * FROM user WHERE user_id = :user_id"
    params = {"user_id": user_id}
    db.execute(qry, params)
    row = db.fetchone()
    if not row:
        raise MissingUser(user_id)
    return row_to_model(row)


def get_all_users() -> list[User]:
    qry = "SELECT * FROM user"
    db.execute(qry)
    return [row_to_model(row) for row in db.fetchall()]


def create_user(user: UserCreate) -> User:
    """Add <user> to user table"""
    qry = "INSERT INTO user (name, hash) VALUES (:name, :hash)"
    params = model_to_dict(user)
    try:
        db.execute(qry, params)
        user_id = db.lastrowid()
        return get_single_user(user_id)
    except IntegrityError:
        raise DuplicateUser(user)


def modify_user(user_id: int, user: User) -> User:
    qry = """UPDATE user
             SET name = :name, hash = :hash
             WHERE user_id = :user_id"""
    params = {"user_id": user_id, "name": user.name, "hash": user.hash}
    res = db.execute(qry, params)
    if res.rowcount == 0:
        raise MissingUser(user_id)
    return get_single_user(user_id)


def delete_user(user_id: int) -> None:
    """Drop user with <user_id> from user table"""
    qry = "DELETE FROM user WHERE user_id = :user_id"
    params = {"user_id": user_id}
    res = db.execute(qry, params)
    if res.rowcount == 0:
        raise MissingUser(user_id)


def delete_all_users() -> None:
    """Drop all users from user table"""
    qry = "DELETE FROM user"
    db.execute(qry)
