from jose import jwt,JWTError
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
# from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
import app.database as database
from app.Schema import token,user
from app.models import Users

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = "nguyenthuy_secretkey_ecommerce_30062023"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def create_access_token(data:dict):
    data_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data_encode.update({"exp": expire})
    encode_jwt = jwt.encode(data_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encode_jwt


def verify_access_token(data:str,credentials_exception):
    try:
        payload = jwt.decode(data,SECRET_KEY,algorithms=ALGORITHM)
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception

        token_data = token.TokenData(id=id)
    except JWTError:
            raise credentials_exception
    
    return token_data


# def get_current_user(token: str, db: Session = Depends(database.get_db())):
#     try:
#         user_id = verify_access_token(token).id
#         user = db.query(Users).get(user_id)
#         return user
#     except:
#         pass


def get_current_user(token:str = Depends(oauth2_scheme),
                     response_model= user.UserOut,
                     db:Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail='Could not validate credentials',
                                          headers={"WWW-Authenticate":"Bearer"})
    token = verify_access_token(token,credentials_exception)
    user = db.query(Users).filter(Users.id == token.id).first()
    
    return user
