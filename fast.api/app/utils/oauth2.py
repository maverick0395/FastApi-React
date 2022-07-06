from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from pydantic import ValidationError
from sqlalchemy.orm import Session
from app.schema import TokenData, UserOut
from app.database import get_db
from app.services.auth import AuthService
from ..config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.JWT_SECRET
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY)
    except JWTError:
        raise credentials_exception from None
    
    user_data = payload.get('user')
    
    try:
        user = UserOut.parse_obj(user_data)
    except ValidationError:
        raise credentials_exception from None
    
    return user

# def get_current_user(
#     token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
# ):    
#     credentials_exception = HTTPException(
#         status_code=404,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     token = verify_access_token(token, credentials_exception)
#     user = db.query(User).filter_by(id=token.id).first()

#     return user

def get_current_user(token: str = Depends(oauth2_scheme)) -> UserOut:
     return verify_access_token(token)