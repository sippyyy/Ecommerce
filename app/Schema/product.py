from pydantic import BaseModel, HttpUrl
from fastapi import Form,UploadFile,File

class Image(BaseModel):
    url: HttpUrl
    name: str


class Product(BaseModel):
    product_name: str = Form(...)
    price: float = Form(...)
    product_type: str  = Form(...)
    detail: str = Form(...)
    quantity: int = Form(...)
    image: UploadFile | None = None
    

