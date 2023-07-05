from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List
from app import database, models,oauth2,untils
from app.Schema import cart
import logging


routers = APIRouter(
    prefix='/carts',
    tags=['carts']
)
logging.basicConfig(level=logging.WARNING,
                    filename="log.log",
                    filemode='w',
                    format='%(asctime)s- %(levelname)s- %(message)s')

@routers.get('/',
             status_code= status.HTTP_200_OK,
             response_model= List[cart.CartOut])
def get_cart(db : Session = Depends(database.get_db),
             current_user= Depends(oauth2.get_current_user)):
    carts = db.query(models.Carts).filter(models.Carts.user_id == current_user.id).all()
    logging.warn(f"Carts: {carts}")
    return carts


@routers.post('/',
              status_code= status.HTTP_201_CREATED)
def create_cart(cart: cart.CartIn,
                db: Session = Depends(database.get_db),
                current_user= Depends(oauth2.get_current_user)):
    product = db.query(models.Products).filter(models.Products.id == cart.product_id).first()
    untils.check_if_dont_exist(product)
    untils.check_user_validation(cart.user_id, current_user)
    cart_exist_product_db = db.query(models.Carts
                                    ).filter(models.Carts.product_id == cart.product_id
                                    ).filter(models.Carts.user_id == current_user.id)
    cart_exist_product = cart_exist_product_db.first()
    if cart_exist_product:
        cart.order_qty = cart.order_qty + cart_exist_product.order_qty
        cart_exist_product_db.update(cart.dict(),synchronize_session=False)
    else:
        new_cart = models.Carts(**cart.dict())
        db.add(new_cart)
    db.commit()
    
    return {'message': 'Create cart successfully'}    


@routers.put('/{id}',
             status_code=status.HTTP_204_NO_CONTENT)
def edit_cart(id:int,
              data:cart.CartEdit,
              db: Session = Depends(database.get_db),
              current_user= Depends(oauth2.get_current_user)):
    cart_db = db.query(models.Carts).filter(models.Carts.id == id)
    cart = cart_db.first()
    untils.check_if_dont_exist(cart)
    untils.check_user_validation(cart.user_id, current_user)
    if data.order_qty ==0:
        db.delete(cart)
    else:
        cart_db.update(data.dict(),synchronize_session=False)
    db.commit()
    return

@routers.delete('/{id}',
                status_code=status.HTTP_204_NO_CONTENT)
def delete_cart(id:int,
                db :  Session = Depends(database.get_db),
                current_user= Depends(oauth2.get_current_user)):
    cart = db.query(models.Carts).filter(models.Carts.id == id).first()
    untils.check_if_dont_exist(cart)
    untils.check_user_validation(cart.user_id, current_user)
    db.delete(cart)
    db.commit()
    return

