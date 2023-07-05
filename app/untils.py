from passlib.context import CryptContext
from fastapi import HTTPException,status

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashPassword(password):
    return pwd_context.hash(password)

def verify(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

def check_user_validation(user_response, current_user):
    if user_response != current_user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"You dont have permission")
        
def check_if_dont_exist(check_item):
    if not check_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Not found")
