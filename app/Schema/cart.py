from pydantic import BaseModel
from .product import Product

class CartIn(BaseModel):
    product_id: int
    user_id: int
    order_qty: int
    

class CartEdit(BaseModel):
    order_qty: int

class CartOut(BaseModel):
    id: int
    product_id: int
    order_qty:int
    product_detail:Product
    class Config:
        orm_mode = True
    