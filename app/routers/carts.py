from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List
from app import database, models,oauth2
from app.Schema import cart

routers = APIRouter(
    prefix='/carts',
    tags=['carts']
)

@routers.get('/',
             status_code= status.HTTP_200_OK,
             response_model= List[cart.CartOut])
def get_cart(db : Session = Depends(database.get_db),
             current_user= Depends(oauth2.get_current_user)):
    carts = db.query(models.Carts).filter(models.Carts.user_id == current_user.id).all()
    return carts


@routers.post('/',
              status_code= status.HTTP_201_CREATED)
def create_cart(cart: cart.CartIn,
                db: Session = Depends(database.get_db),
                current_user= Depends(oauth2.get_current_user)):
    product = db.query(models.Products).filter(models.Products.id == cart.product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Product id {cart.product_id} not found")
    if cart.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"You are not allowed to create this cart")
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
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Cart {id} not found")
    if current_user.id != cart.user_id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            detail=f"You are not allowed to edit infomation of this cart")
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
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Cart not found")
    if cart.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail= "You are not allowed to delete this cart")
    db.delete(cart)
    db.commit()
    return

