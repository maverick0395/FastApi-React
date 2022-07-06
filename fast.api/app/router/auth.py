# from shutil import unregister_archive_format
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.schema import Token, UserCreate, UserOut
from app.database import get_session
from app.services import AuthService, get_current_user


router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: AuthService = Depends()
):
    return service.authenticate_user(
        form_data.username,
        form_data.password,
    )


@router.post("/register", response_model=Token)
def register(
    user_data: UserCreate, 
    service: AuthService = Depends()
):
    return service.register_new_user(user_data)


@router.post("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/login")

@router.get("/user", response_model=UserOut)
def get_user(user: UserOut = Depends(get_current_user)):
    return user