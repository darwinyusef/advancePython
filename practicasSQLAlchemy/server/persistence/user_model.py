from sqlalchemy import Boolean, Column, Integer, String

from persistence.database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True)
    title = Column(String, default="")
    description = Column(String, default="")
    active = Column(Boolean, default=True)