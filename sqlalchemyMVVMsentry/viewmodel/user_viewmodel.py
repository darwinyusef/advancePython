
# Dependency to get a database session

from models.user_model import User
from fastapi import HTTPException, status
from schemas.user_schema import UserCreate, UserUpdate
from docs.user_docs import USERS
import sentry_sdk

# GET all users
def getUser(db):
    return db.query(User).all()

# GET a single user by ID


def getShowUser(db, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=USERS['gs-into-detail'])
    return db_user

# Create a single user


def postUser(db, user: UserCreate):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=USERS['p-into-detail'])

    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Update a single user


def putUser(db, user: UserUpdate, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=USERS['pu-into-detail'])

    for field in user.dict().keys():
        setattr(db_user, field, getattr(user, field))

    db.commit()
    db.refresh(db_user)
    return db_user

# Delete a single user


def deleteUser(db, user_id: int):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=USERS['d-into-detail'])

    db.delete(db_user)
    db.commit()
    return {"message": USERS['d-response']}


def sentryError():
    try:
        result = 1 / 0
    except ZeroDivisionError as e:
        sentry_sdk.capture_exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

    return {"message": "This should not be reached"}
