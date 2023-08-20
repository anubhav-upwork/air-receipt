from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session

from app.crud.user import get_user_info_service, get_user_action_audit_service
from app.schemas.user.user_info import UserInfo, UserInfo_Create

from app.schemas.user.user_action_audit import UserAuditTrail_Create
from app.models.user.user_action_audit import User_Action

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
    audit_log = None
    user = authenticate(email=form_data.username, password=form_data.password, db=db)
    if not user:
        # enter into user audit trail
        audit_log = UserAuditTrail_Create(
            user_id=1,
            action=User_Action.login,
            action_msg=f"Some User tried to log in."
        )

        user_audit = get_user_action_audit_service.create(db, audit_log)

        raise HTTPException(status_code=400, detail="Incorrect username or password")

    # enter into user audit trail
    audit_log = UserAuditTrail_Create(
        user_id=user.id,
        action=User_Action.login,
        action_msg=f"User <{user.user_name}> logged in."
    )

    user_audit = get_user_action_audit_service.create(db, audit_log)

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
    user = get_user_info_service.create(db_session=db, obj_in=user_in)

    return user
