from fastapi import HTTPException, Depends, APIRouter

from app import model, schema
from app.database import get_session
from app.services import get_current_user, oauth2_scheme
from sqlalchemy.orm import Session



router = APIRouter(prefix="/user", tags=["Users"])


@router.post("/", status_code=201, response_model=schema.UserOut)
def create_user(user: schema.UserCreate, db: Session = Depends(get_session)):

    new_user = model.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}", response_model=schema.UserOut)
def get_user(
    id: int,
    db: Session = Depends(get_session),
    token: schema.Token = Depends(oauth2_scheme)
   ):
    user = db.query(model.User).get(id)

    if not user:
        raise HTTPException(status_code=404, detail="This user was not found")

    return user
