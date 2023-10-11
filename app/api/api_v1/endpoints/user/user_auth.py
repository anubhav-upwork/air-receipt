from datetime import datetime
from typing import Any
from pydantic import condecimal

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm.session import Session

# user info,login
from app.models.user.user_info import User_Info
from app.models.user.user_login import User_Login
from app.crud.user import get_user_info_service, get_user_action_audit_service, get_user_login_service
from app.schemas.user.user_info import UserInfo, UserInfo_Create, UserInfo_Update
from app.schemas.user.user_login import UserLogin, UserLogin_Update, UserLogin_Create

# user audit
from app.schemas.user.user_action_audit import UserAuditTrail_Create
from app.models.user.user_action_audit import User_Action
from jose import jwt, JWTError

from app.api import deps
from app.core.auth import (
    authenticate,
    create_access_token,
    create_refresh_token,
    JWT_SECRET,
    ALGORITHM
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", tags=["Authentication"])
def login(db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
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
            action_msg=f"Some User tried to log in with details {form_data.username}."
        )

        user_audit = get_user_action_audit_service.create(db, audit_log)
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    # enter into user audit trail
    audit_log = UserAuditTrail_Create(
        user_id=user.id,
        action=User_Action.login,
        action_msg=f"User <{user.user_name}> logged in."
    )

    # commit to audit table
    user_audit = get_user_action_audit_service.create(db, audit_log)

    # also activate the user in user info
    user_update = UserInfo_Update(
        user_is_active=True
    )
    user_update_request = get_user_info_service.update(db_session=db, _id=user.id, obj=user_update)

    access = create_access_token(sub=user.user_email)
    refresh = create_refresh_token(sub=user.user_email)

    # commit to user login token table, Check if a token already exists, if exists update otherwise create new
    ulog = get_user_login_service.get_by_user_id(db_session=db, user_id=user.id)
    if ulog is not None:
        token_db = get_user_login_service.update(db_session=db, _id=ulog.access_token, obj=UserLogin_Update(
            access_token=access,
            refresh_token=refresh,
            status=True
        ))
    else:
        token_db = get_user_login_service.create(db_session=db, obj_in=UserLogin_Create(
            user_id=user.id,
            access_token=access,
            refresh_token=refresh,
            status=True
        ))
    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "bearer"
    }


@router.get("/me", response_model=UserInfo)
def read_users_me(db: Session = Depends(deps.get_db), current_user: User_Info = Depends(deps.get_current_user)):
    """
    Fetch the current logged-in user.
    """
    # enter into user audit trail
    audit_log = UserAuditTrail_Create(
        user_id=current_user.id,
        action=User_Action.update,
        action_msg=f"User <{current_user.user_name}> accessed get user details."
    )

    user_audit = get_user_action_audit_service.create(db, audit_log)
    return current_user


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


@router.patch("/add_credit", status_code=201, response_model=UserInfo_Update)
async def add_credit(credit: condecimal(decimal_places=2),
                     db: Session = Depends(deps.get_db),
                     current_user: User_Info = Depends(deps.get_current_user)) -> User_Info:
    uinfo = UserInfo_Update(
        user_credit=current_user.user_credit + credit
    )
    if credit < 1.00:
        raise HTTPException(
            status_code=400, detail="Trying to add less than 1 credit!!"
        )

    # enter into user audit trail
    audit_log = UserAuditTrail_Create(
        user_id=current_user.id,
        action=User_Action.credit_load,
        action_msg=f"User <{current_user.user_name}> added credits {credit}."
    )
    user_audit = get_user_action_audit_service.create(db, audit_log)
    return get_user_info_service.update(db_session=db, _id=current_user.id, obj=uinfo)


@router.post('/logout')
def logout(token_tuple=Depends(deps.get_current_user_tuple), db: Session = Depends(deps.get_db)):
    print(f"Payload :::: {token_tuple[1]}")
    # commit to user login token table, Check if a token already exists, if exists update otherwise create new
    ulog = get_user_login_service.get_by_user_id(db_session=db, user_id=token_tuple[0].id)
    if ulog is not None:
        token_db = get_user_login_service.update(db_session=db, _id=ulog.access_token, obj=UserLogin_Update(
            access_token=ulog.access_token,
            refresh_token=ulog.refresh_token,
            status=False
        ))
    else:
        return {"message": f"Logging out Unknown {token_tuple[0].user_name}"}
    return {"message": "Logout Successfully"}
