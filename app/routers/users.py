from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from app.database import get_db
from app.Schema.user import Password,UserIn,UserOut,UserInfo,FullUserOut,UserDetailIn
from app.models import Users
from app.untils import hashPassword,verify,check_user_validation,check_if_dont_exist
from app.oauth2 import get_current_user

routers = APIRouter(
    prefix="/users",
    tags=["users"]
)

@routers.post('/',
              status_code=status.HTTP_201_CREATED,
              response_model=UserOut)
def create_user(user: UserIn, db: Session = Depends(get_db)):
    user.password = hashPassword(user.password)
    new_user = Users(**user.dict())
    db.add(new_user)
    db.commit()
    return new_user

@routers.get('/{id}',status_code=status.HTTP_200_OK,response_model=UserInfo)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.id == id).first()
    check_if_dont_exist(user)
    return user

@routers.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db),current_user:int = Depends(get_current_user)):
    user_delete = db.query(Users).filter(Users.id == id).first()
    check_user_validation(id,current_user)
    check_if_dont_exist(user_delete)
    db.delete(user_delete)
    db.commit()
    return {"message": f"Delete user {id} successfully"}

@routers.put('/{id}',status_code=status.HTTP_201_CREATED,response_model=FullUserOut)
def edit_user(id:int, user: UserDetailIn, db: Session = Depends(get_db), current_user:int = Depends(get_current_user)):
    user_edit_db = db.query(Users).filter(Users.id == id)
    check_if_dont_exist(user_edit_db.first())
    check_user_validation(user_edit_db.first().id,current_user)
    user_edit_db.update(user.dict(),synchronize_session=False)
    db.commit()
    return user_edit_db.first()
    
@routers.put('/password/{id}',status_code=status.HTTP_204_NO_CONTENT)
def change_password(id:int,password: Password, db: Session = Depends(get_db), current_user:int = Depends(get_current_user)):
    user_edit_db = db.query(Users).filter(Users.id == current_user.id)
    user = user_edit_db.first()
    check_user_validation(user.id,current_user)
    check_if_dont_exist(user)
    if not verify(password.old_password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Password unmatch")
    if verify(password.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="New password cannot be same as old password")
    user_edit_db.update({"password":hashPassword(password.password)},synchronize_session=False)
    db.commit()
    return
