from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional

# LOGIN SCHEMA
class User(BaseModel):
    user_name: str
    password: str
    

# CHANGE PASSWORD
class Password(BaseModel):
    old_password: str
    password: str

# REGISTER SCHEMA
class UserIn(User):
    email: EmailStr
    is_activated: bool
    is_seller:  bool = False

# USER INFO RETURN
class UserInfo(BaseModel):
    full_name: Optional[str]
    phone: Optional[str]
    email: str
    address: Optional[str]
    is_activated: bool
    is_seller:  bool
    class Config:
        orm_mode = True
# CURRENT_USER INFO
class UserOut(BaseModel):
    id: int
    user_name: str
    is_activated: bool
    created_at: datetime
    is_seller:  bool
    class Config:
        orm_mode = True

# FULL USER INFO DETAIL
class FullUserOut(BaseModel):
    id: int
    user_name:str
    full_name: str
    phone: str
    email: str
    address: str
    is_activated: bool
    is_seller:  bool
    class Config:
        orm_mode = True
     
# FORCE    
class UserDetailIn(BaseModel):
    full_name: str
    phone: str
    email: str
    address: str
    is_activated: bool
