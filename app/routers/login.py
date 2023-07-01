from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app import models,untils,oauth2,database
routers = APIRouter(tags=['Authentication'])

@routers.post('/login',status_code=status.HTTP_200_OK)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(),db:Session = Depends(database.get_db)) :
    user_login = db.query(models.Users).filter(models.Users.user_name == user_credentials.username).first()
    if user_login is None :
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    if not untils.verify(user_credentials.password,user_login.password):
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="User name or Password is not correct!!")
    access_token = oauth2.create_access_token(data = {"user_id":user_login.id})
    
    return {"access_token": access_token, "token_type": "bearer"}
