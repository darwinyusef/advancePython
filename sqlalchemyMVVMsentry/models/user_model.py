from sqlalchemy import Column, Integer, String, Boolean, DateTime
from config.database import Base 

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, default="")
    password = Column(String) 
    is_active = Column(Boolean, default=True)
    verifymail = Column(String, default=True)
    create_at = Column(DateTime, default="now")
    update_at = Column(DateTime, default="now")    
    
    def __repr__(self):
        return f"<User {self.id} - {self.email}>"