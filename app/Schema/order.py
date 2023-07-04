from pydantic import BaseModel
from .product import Product

class Order(BaseModel):
    user_id: int
    product_id: int
    order_qty: int
    
class OrderChange(BaseModel):
    order_qty: int

class OrderOut(Order):
    id: int
    product_detail:Product
    class Config:
        orm_mode = True
    
