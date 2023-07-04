from fastapi import APIRouter, HTTPException,status,Depends
from sqlalchemy.orm import Session
from app import database,models,oauth2
from app.Schema import order
from typing import List

routers = APIRouter(
    prefix='/orders',
    tags=['orders']
)

@routers.get('/',status_code = status.HTTP_200_OK,
             response_model=List[order.OrderOut])
def get_orders(db: Session = Depends(database.get_db),
               current_user:int = Depends(oauth2.get_current_user)):
    orders = db.query(models.Orders).filter(models.Orders.user_id == current_user.id).all()
    return orders

@routers.post('/',status_code = status.HTTP_201_CREATED)
def create_orders(order: order.Order,
                  db: Session = Depends(database.get_db),
                  current_user:int = Depends(oauth2.get_current_user)):
    user_order = db.query(models.Users).filter(models.Users.id == current_user.id).first()
    product_order = db.query(models.Products).filter(models.Products.id == order.product_id).first()
    if not user_order.address or not user_order.phone:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Complete your info account before place order") 
    if not product_order:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"Product id {order.product_id} not found")
    
    if product_order.quantity < order.order_qty:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"Can not order more than available product quantity")
    new_order = models.Orders(**order.dict())
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return {"message":"Order completed!"}

@routers.put('/{id}',status_code=status.HTTP_201_CREATED)
def edit_order(id:int,
               data: order.OrderChange,
               db: Session = Depends(database.get_db),
               current_user:int = Depends(oauth2.get_current_user)):
    order_db = db.query(models.Orders).filter(models.Orders.id == id)
    order = order_db.first()
    if not order:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            details = "Order not found")
    if order.user_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                            details = "You are not allowed to edit infomation of this order")
    if data.order_qty == 0:
            db.delete(order)
            db.commit()
    order_db.update(data.dict(),synchronize_session=False)
    db.commit()
    return {"message":"Order changed!"}

@routers.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_order(id:int,
                 db: Session = Depends(database.get_db),
                 current_user:int = Depends(oauth2.get_current_user)):
    order = db.query(models.Orders).filter(models.Orders.id == id).first()
    if not order:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            details="Order not found")
    if order.user_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                            details="You are not allow to delete this order")
    db.delete(order)
    db.commit()
     