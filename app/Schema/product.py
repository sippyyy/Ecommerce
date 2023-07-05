from pydantic import BaseModel, HttpUrl
from fastapi import Form,UploadFile,File
from .user import FullUserOut
from typing import Optional


class Product(BaseModel):
    id: int
    product_name: str
    price: float
    product_type: str 
    detail: str
    quantity: int
    image: str 
    seller_id: int
    seller_info: FullUserOut
    class Config:
        orm_mode = True
        
class ProductOut(BaseModel):
    Products: Product
    all_ordered_qty: Optional[int]
    class Config:
        orm_mode = True
    

