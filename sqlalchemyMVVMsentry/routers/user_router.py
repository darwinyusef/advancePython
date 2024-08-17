from fastapi import APIRouter,  Depends, status, Path
from typing import Annotated, Optional, Union
from sqlalchemy.orm import Session

from config.database import get_db
from schemas.user_schema import UserCreate, UserOut, UserUpdate
from viewmodel.user_viewmodel import getUser, getShowUser, postUser, putUser, deleteUser, sentryError
from docs.user_docs import USERS

router = APIRouter(
    prefix="/users",
    tags=["Usuarios"],
    responses={404: {"description": "Not found"}}
)

# DB connection


def get_db_session():
    db = next(get_db())
    yield db

# get user


@router.get("/", response_model=list[UserOut], summary=USERS["g-sum"], response_description=USERS["g-res"], description=USERS["g-desc"])
def get_all_users(db: Session = Depends(get_db_session)):
    db_users = getUser(db)
    return db_users

# get show user

@router.get("/search")
def read_item(q: Union[int, None] = None):
    return {"q": q}


@router.get("/{user_id}", response_model=UserOut, summary=USERS["gs-sum"], response_description=USERS["gs-res"], description=USERS["gs-desc"])
def read_user(
    user_id:  Annotated[int, Path(description="user_id ID del usuario")],
    db: Session = Depends(get_db_session)
):
    user = getShowUser(db, user_id)
    return user




# post user
@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED, summary=USERS["p-sum"], response_description=USERS["p-res"], description=USERS["p-desc"])
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db_session)
):
    user = postUser(db, user)
    return user

# put user into database


@router.put("/{user_id}",
            response_model=UserOut, summary=USERS["pu-sum"], response_description=USERS["pu-res"], description=USERS["pu-desc"])
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db_session)):
    update = putUser(db, user, user_id)
    return update

# delete user
@router.delete("/{user_id}",
               summary="Elimina un usuario",
               response_description="El usuario ha sido eliminado satisfactoriamente",
               description="Elimina un usuarios a través de un ID")
def delete_user(user_id: int, db: Session = Depends(get_db_session)):
    delete = deleteUser(db, user_id)
    return delete


@router.get("/errorcito")
def prError():
    return sentryError()
