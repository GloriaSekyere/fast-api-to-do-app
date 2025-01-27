import os
from fastapi import APIRouter, HTTPException
from model.user import User, UserCreate, UserUpdate

if os.getenv("TODO_UNIT_TEST"):
    from fake import user as service
else:
    from service import user as service
from error import MissingUser, DuplicateUser


router = APIRouter(prefix="/user")


@router.get("")
@router.get("/")
def get_all_users() -> list[User]:
    return service.get_all_users()


@router.get("/{user_id}")
def get_single_user(user_id: int) -> User:
    try:
        return service.get_single_user(user_id)
    except MissingUser as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.post("", status_code=201)
@router.post("/", status_code=201)
def create_user(user: UserCreate) -> User:
    try:
        return service.create_user(user)
    except DuplicateUser as exc:
        raise HTTPException(status_code=409, detail=exc.msg)


@router.patch("/{user_id}")
def modify_user(user_id: int, user: UserUpdate) -> User:
    try:
        return service.modify_user(user_id, user)
    except MissingUser as exc:
        raise HTTPException(status_code=404, detail=exc.msg)
    except DuplicateUser as exc:
        raise HTTPException(status_code=409, detail=exc.msg)


@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int) -> None:
    try:
        service.delete_user(user_id)
    except MissingUser as exc:
        raise HTTPException(status_code=404, detail=exc.msg)


@router.delete("", status_code=204)
@router.delete("/")
def delete_all_users() -> None:
    service.delete_all_users()
