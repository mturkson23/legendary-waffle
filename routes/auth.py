from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status, APIRouter
import bcrypt
from sqlalchemy.orm import Session

from controllers import get_user_by_username, create_user
from schemas import UserCreateRequest, UserResponse
from database import get_db

router = APIRouter(prefix="/auth")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    db_user = get_user_by_username(db, username=token)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect username or password",
        )
    return UserResponse(username=db_user.username, id=db_user.id)


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    db_user = get_user_by_username(db, username=form_data.username)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect username or password",
        )
    if not bcrypt.checkpw(form_data.password.encode("utf-8"), db_user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect username or password",
        )
    return {"access_token": db_user.username, "token_type": "bearer"}


@router.post("/register")
def register(user: UserCreateRequest, db: Session = Depends(get_db)):
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
        )
    new_user = create_user(db=db, user=user)
    return {"access_token": new_user.username, "token_type": "bearer"}


@router.get("/profile")
def get_my_profile(current_user: UserResponse = Depends(get_current_user)):
    return current_user

# To be checked out later
# @router.get("/logout")
# def logout():
#     return {"message": "Logged out successfully"}
