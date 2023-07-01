from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from app.database import get_db
from app.Schema.user import UserIn,UserOut,UserInfo,FullUserOut
from app.models import Users
from app.untils import hashPassword
from app.oauth2 import get_current_user

routers = APIRouter(
    prefix="/users",
    tags=["users"]
)

@routers.post('/',status_code=status.HTTP_201_CREATED)
def create_user(user: UserIn, db: Session = Depends(get_db)):
    user.password = hashPassword(user.password)
    new_user = Users(**user.dict())
    db.add(new_user)
    db.commit()
    return {"message": "Create user successfully"}

@routers.get('/{id}',status_code=status.HTTP_200_OK,response_model=FullUserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.id == id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {id} not found")
    return user

@routers.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db),current_user:int = Depends(get_current_user)):
    user_delete = db.query(Users).filter(Users.id == id).first()
    if id != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"You are not allowed to delete this user")
    if user_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User {id} not found")
    db.delete(user_delete)
    db.commit()
    return {"message": f"Delete user {id} successfully"}

@routers.put('/{id}',status_code=status.HTTP_201_CREATED,response_model=FullUserOut)
def edit_user(id:int, user: UserInfo, db: Session = Depends(get_db), current_user:int = Depends(get_current_user)):
    user_edit_db = db.query(Users).filter(Users.id == id)
    if user_edit_db.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User {id} not found")
    if user_edit_db.first().id != current_user.id:
        raise HTTPException(user_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"You are not allowed to edit infomation of this user")
    user_edit_db.update(user.dict(),synchronize_session=False)
    db.commit()
    return user_edit_db.first()
    