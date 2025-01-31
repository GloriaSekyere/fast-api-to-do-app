import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import jwt
from model.user import User, UserCreate, UserUpdate

load_dotenv()
if os.getenv("TODO_UNIT_TEST"):
    from fake import user as data
else:
    from data import user as data


# AUTH
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain: str, hash: str) -> bool:
    """Hash <plain> and compare with <hash> from the database"""
    return pwd_context.verify(plain, hash)


def get_hash(plain: str) -> str:
    """Return the hash of a <plain> string"""
    return pwd_context.hash(plain)


def get_jwt_username(token: str) -> str | None:
    """Return username from JWT access <token>"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if not (username := payload.get("sub")):
            return None
    except jwt.JWTError:
        return None
    return username


def get_current_user(token: str) -> User | None:
    """Decode an OAuth access <token> and return the User"""
    if not (username := get_jwt_username(token)):
        return None
    if user := lookup_user(username):
        return user
    return None


def lookup_user(name: str) -> User | None:
    """Return a matching User from the database for <name>"""
    if user := data.get_user_by_name(name):
        return user
    return None


def auth_user(name: int, plain: str) -> User | None:
    """Authenticate user <name> and <plain> password"""
    if not (user := lookup_user(name)):
        return None
    if not verify_password(plain, user.hash):
        return None
    return user


def create_access_token(data: dict, expires: timedelta | None = None):
    """Return a JWT access token"""
    src = data.copy()
    now = datetime.now(timezone.utc)
    if not expires:
        expires = timedelta(minutes=15)
    src.update({"exp": now + expires})
    encoded_jwt = jwt.encode(src, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# CRUD
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
