
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(default="usernamevalido")
    is_active:  bool = True
    verifymail: str = Field(default="")
    create_at: datetime = Field(default_factory=datetime.utcnow)
    update_at: datetime = Field(default_factory=datetime.utcnow)
   
# UserCreate: Used for creating users, including password.
class UserCreate(UserBase):
    password: str

# UserUpdate: Used for updating users, with an optional password field.
class UserUpdate(UserBase):
    password: Optional[str] = None

# UserOut: Used for updating users, with an id field.
class UserOut(UserBase):
    id: int = Field(default=1)
