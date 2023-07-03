from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional
from enum import Enum

class User(BaseModel):
    user_name: str
    password: str
    
    
class UserIn(User):
    email: EmailStr
    is_activated: bool
    is_seller:  bool = False
    
class UserInfo(BaseModel):
    full_name: str
    phone: str
    email: str
    address: str
    is_activated: bool
    is_seller:  bool

class UserOut(BaseModel):
    id: int
    user_name: str
    is_activated: bool
    created_at: datetime
    is_seller:  bool
    
    
    class Config:
        orm_mode = True


class FullUserOut(UserInfo):
    id: int
    user_name: str

    class Config:
        orm_mode = True
