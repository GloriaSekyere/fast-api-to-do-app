from pydantic import BaseModel


class User(BaseModel):
    user_id: int
    name: str
    hash: str


class UserCreate(BaseModel):
    name: str
    hash: str


class UserUpdate(BaseModel):
    name: str | None = None
    hash: str | None = None
