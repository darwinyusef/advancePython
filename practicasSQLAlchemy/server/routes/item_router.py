from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas import user_shema
from persistence.database import get_db
from domain.item_domain import get_items, create_item

router = APIRouter(
    prefix="/item",
    tags=["Items"],
    responses={404: {"description": "Not found"}}
)


@router.get("/", response_model=list[user_shema.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = get_items(db, skip=skip, limit=limit)
    return items


@router.post("/ ", response_model=user_shema.Item)
def create_item_for_user(item: user_shema.ItemCreate, db: Session = Depends(get_db)
): 
    return create_item(db=db, item=item)