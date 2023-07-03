from fastapi import APIRouter, HTTPException, Depends, status, Form, UploadFile, File
from sqlalchemy.orm import Session
from app import models, database, oauth2
from app.Schema.product import Product
from secrets import token_hex
from typing import List
from app.service.gcs import GCStorage
import os
import urllib.parse
routers = APIRouter(
    prefix='/products',
    tags=['products']
)


@routers.get('/', status_code=status.HTTP_200_OK, response_model=List[Product])
def get_products(limit: int = 20,
                 skip: int = 0,
                 search_name: str = "",
                 search_type: str = "",
                 db: Session = Depends(database.get_db)):
    products = db.query(
        models.Products
    ).filter(
        models.Products.product_name.contains(
            search_name
        )
    ).filter(
        models.Products.product_type.contains(
            search_name
        )
    ).limit(
        limit
    ).offset(
        skip
    ).all()
    return products


@routers.post('/', status_code=status.HTTP_201_CREATED)
async def create_product(product_name: str = Form(...),
                         price: float = Form(...),
                         product_type: str = Form(...),
                         detail: str = Form(...),
                         quantity: int = Form(...),
                         image: UploadFile = File(...),
                         db: Session = Depends(database.get_db),
                         current_user=Depends(oauth2.get_current_user)):
    if not current_user.is_seller:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"You don't have permission to sell this product")
    image_path = GCStorage().upload_file(image)
    new_product = models.Products(
        product_name=product_name,
        price=price,
        product_type=product_type,
        detail=detail,
        quantity=quantity,
        image=image_path,
        seller_id=current_user.id
    )
    db.add(new_product)
    db.commit()
    return {"message": "Create product successfully"}


@routers.delete('/{id}',status_code = status.HTTP_204_NO_CONTENT)
def delete_product(id:int,
                   db: Session = Depends(database.get_db),
                   current_user=Depends(oauth2.get_current_user)):
    product = db.query(models.Products).filter(models.Products.id == id).first()
    if product.seller_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"You are not allowed to delete this product")
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product {id} not found")
    file_path = os.path.basename(urllib.parse.unquote(product.image))
    GCStorage().delete_file(bucket_name="ecommerce_sippyyy", file_path=file_path)
    db.delete(product)
    db.commit()
    return {"message": f"Delete product {id} successfully"}
    