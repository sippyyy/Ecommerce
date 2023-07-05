from fastapi import APIRouter, HTTPException, Depends, status, Form, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models, database, oauth2,untils
from app.Schema.product import Product,ProductOut
from typing import List,Optional
from app.service.gcs import GCStorage
import os
import urllib.parse
routers = APIRouter(
    prefix='/products',
    tags=['products']
)


@routers.get('/', status_code=status.HTTP_200_OK,
             response_model=List[ProductOut])
def get_products(limit: int = 20,
                 skip: int = 0,
                 search_name: str = "",
                 search_type: str = "",
                 db: Session = Depends(database.get_db)):
    products = db.query(models.Products,func.sum(models.Orders.order_qty).label("all_ordered_qty")
                        ).join(models.Orders,models.Products.id == models.Orders.product_id, isouter=True
                               ).group_by(models.Products.id,models.Orders.product_id,models.Orders.order_qty
                                          ).filter(models.Products.product_name.
                                                contains(search_name)
                                                ).filter(models.Products.product_type.
                                                         contains(search_name)
                                                         ).limit(limit
                                                                 ).offset(skip
                                                                          ).all()
    
    # print(products)
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
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"You don't have permission to sell this product")
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
    untils.check_user_validation(product.seller_id,current_user)
    untils.check_if_dont_exist(product)
    file_path = os.path.basename(urllib.parse.unquote(product.image))
    GCStorage().delete_file(file_path=file_path)
    db.delete(product)
    db.commit()
    return {"message": f"Delete product {id} successfully"}


@routers.put('/{id}',status_code=status.HTTP_200_OK,
             response_model=Product) 
def edit_product(id:int,
                product_name:Optional[str] = Form(...),
                price: Optional[float] = Form(...),
                product_type: Optional[str] = Form(...),
                detail: Optional[str] = Form(...),
                quantity: Optional[int] = Form(...),
                image: Optional[UploadFile] = File(...),
                db: Session = Depends(database.get_db),
                current_user=Depends(oauth2.get_current_user)):
    product = db.query(models.Products).filter(models.Products.id == id)
    product_result = product.first()
    untils.check_if_dont_exist(product_result)
    untils.check_user_validation(product_result.seller_id,current_user)
    current_file_path = os.path.basename(urllib.parse.unquote(product_result.image))
    image_path = GCStorage().edit_file(current_file_path,image)
    product.update({"product_name":product_name,
                    "price":price,
                    "product_type":product_type,
                    "detail":detail,
                    "quantity":quantity,
                    "image":image_path
                    })
    db.commit()
    return product_result
    