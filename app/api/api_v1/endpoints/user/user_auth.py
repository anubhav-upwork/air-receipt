from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session

from app.crud.user import get_user_info_service
from app.schemas.user.user_info import UserInfo, UserInfo_Create
from app.api import deps
from app.core.auth import (
    authenticate,
    create_access_token,
)

from app.models.user.user_info import User_Info

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", tags=["Authentication"])
def login(
        db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    Get the JWT for a user with data from OAuth2 request form body.
    """

    user = authenticate(email=form_data.username, password=form_data.password, db=db)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {
        "access_token": create_access_token(sub=user.user_email),
        "token_type": "bearer",
    }


@router.get("/me", response_model=UserInfo)
def read_users_me(current_user: UserInfo = Depends(deps.get_current_user)):
    """
    Fetch the current logged-in user.
    """

    user = current_user
    return user


@router.post("/signup", response_model=UserInfo, status_code=201)
def create_user_signup(
        *,
        db: Session = Depends(deps.get_db),
        user_in: UserInfo_Create,
) -> Any:
    """
    Create new user without the need to be logged in.
    """

    user = db.query(User_Info).filter(User_Info.user_email == user_in.user_email).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system",
        )
    user = get_user_info_service.create(db=db, obj_in=user_in)

    return user
