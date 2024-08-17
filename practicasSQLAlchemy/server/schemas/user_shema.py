from pydantic import BaseModel

class ItemBase(BaseModel):
    title: str
    description: str 
    active: bool

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int

