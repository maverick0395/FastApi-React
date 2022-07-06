from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.hash import bcrypt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.database import get_session
from app.config import settings
from app.schema import Token, UserCreate, UserOut
from app.model import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)) -> UserOut:
    return AuthService.verify_access_token(token)


class AuthService:
    @classmethod
    def verify_password(cls, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(plain_password, hashed_password)
    
    
    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)
    
    
    @classmethod
    def verify_access_token(cls, token: str) -> UserOut:
        exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET
            )
        except JWTError:
            raise exception from None

        user_data = payload.get('user')

        try:
            user = UserOut.parse_obj(user_data)
        except ValidationError:
            raise exception from None

        return user

    @classmethod
    def create_access_token(cls, user: User) -> Token:
        user_data = UserOut.from_orm(user)
        now = datetime.utcnow()
        payload = {
            'iat': now,
            'nbf': now,
            'exp': now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            'sub': str(user_data.id),
            'user': user_data.dict(),
        }
        token = jwt.encode(
            payload,
            settings.JWT_SECRET,
        )
        return Token(access_token=token)
    
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session


    def register_new_user(self, user_data: UserCreate) -> Token:
        user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=self.hash_password(user_data.password)
            )
        self.session.add(user)
        self.session.commit()

        return self.create_access_token(user)

    def authenticate_user(self, username: str, password: str) -> Token:
        exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
        )
        user = (
            self.session
            .query(User)
            .filter(User.username == username)
            .first()
        )
        if not user:
            raise exception
        if not self.verify_password(password, user.password):
            raise exception

        return self.create_access_token(user)