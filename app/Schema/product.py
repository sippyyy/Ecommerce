from pydantic import BaseModel, HttpUrl
from fastapi import Form,UploadFile,File
from .user import UserOut


class Product(BaseModel):
    id: int
    product_name: str
    price: float
    product_type: str 
    detail: str
    quantity: int
    image: str 
    seller_id: int
    seller_info: UserOut
    class Config:
        orm_mode = True
