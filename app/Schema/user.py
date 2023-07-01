from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional

class User(BaseModel):
    user_name: str
    password: str
    
    
class UserIn(BaseModel):
    user_name: str
    password: str
    email: EmailStr
    is_activated: bool
    
class UserInfo(BaseModel):
    full_name: str
    phone: str
    email: str
    address: str
    is_activated: bool

class UserOut(BaseModel):
    id: int
    user_name: str
    is_activated: bool
    created_at: datetime
    
    class Config:
        orm_mode = True


class FullUserOut(BaseModel):
    full_name: str
    phone: str
    email: str
    address: str
    is_activated: bool
    id: int
    user_name: str

    class Config:
        orm_mode = True
