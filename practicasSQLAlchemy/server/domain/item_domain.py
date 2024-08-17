from sqlalchemy.orm import Session
from fastapi import Depends
from schemas import user_shema
from persistence.user_model import Item
from persistence.database import get_db


# Dependency to get a database session
def get_db_session():
    db = next(get_db())
    yield db


def get_items(db: Session = Depends(get_db_session), skip: int = 0, limit: int = 100):
    return db.query(Item).offset(skip).limit(limit).all()


def create_item(item: user_shema.ItemCreate, db: Session = Depends(get_db_session)):
    db_item = Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
