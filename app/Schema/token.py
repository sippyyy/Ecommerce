from pydantic import BaseModel,EmailStr
from typing import Optional

class Token(BaseModel):
    token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str]
