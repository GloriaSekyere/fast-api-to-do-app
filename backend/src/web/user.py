import os
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from model.user import User, UserCreate, UserUpdate
from datetime import timedelta

if os.getenv("TODO_UNIT_TEST"):
    from fake import user as service
else:
    from service import user as service
from error import MissingUser, DuplicateUser


ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(prefix="/user")


# This dependency makes a post to "/user/token"
# (from a form containing a username and password)
# and returns an access token.
oauth2_dep = OAuth2PasswordBearer(tokenUrl="token")


def unauthed():
    raise HTTPException(
        status_code=401,
        detail="Incorrect name or password",
        headers={"WWW-Authenticate": "Bearer"},
    )


# This endpoint is directed to by any call that has the
# oauth2_dep() dependency:
@router.post("/token")
def create_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """Get username and password from OAuth form, return access token"""
    user = service.auth_user(form_data.username, form_data.password)
    if not user:
        unauthed()
    expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = service.create_access_token(data={"sub": user.name}, expires=expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/token")
def get_access_token(token: str = Depends(oauth2_dep)) -> dict:
    """Return the current access token"""
    return {"token": token}


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
