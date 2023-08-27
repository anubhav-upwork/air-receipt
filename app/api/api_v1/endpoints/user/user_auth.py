from typing import Any
from pydantic import condecimal

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm.session import Session

# user info,login
from app.crud.user import get_user_info_service, get_user_action_audit_service, get_user_login_service
from app.schemas.user.user_info import UserInfo, UserInfo_Create, UserInfo_Update
from app.schemas.user.user_login import UserLogin, UserLogin_Update, UserLogin_Create

# user audit
from app.schemas.user.user_action_audit import UserAuditTrail_Create
from app.models.user.user_action_audit import User_Action

from app.api import deps
from jose import jwt
from app.core.auth import (
    authenticate,
    create_access_token,
    create_refresh_token,
    JWT_SECRET,
    ALGORITHM
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

    # also activate the user in user info
    user_update = UserInfo_Update(
        user_is_active=True
    )
    user_update_request = get_user_info_service.update(db_session=db, _id=user.id, obj=user_update)

    access = create_access_token(sub=user.user_email)
    refresh = create_refresh_token(sub=user.user_email)

    user_login = UserLogin_Create(
        user_id=user.id,
        access_token=access,
        refresh_token=refresh,
        status=True
    )
    token_db = get_user_login_service.create(db_session=db, obj_in=user_login)
    return {
        "access_token": access,
        "refresh_token": refresh,
        "token_type": "bearer"
    }


@router.get("/me", response_model=UserInfo)
def read_users_me(db: Session = Depends(deps.get_db), current_user: UserInfo = Depends(deps.get_current_user)):
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
                     current_user: UserInfo = Depends(deps.get_current_user)) -> User_Info:
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
def logout(dependencies=Depends(OAuth2PasswordBearer), db: Session = Depends(deps.get_db)):
    # token = dependencies
    # payload = jwt.decode(token, JWT_SECRET, ALGORITHM)
    # print(f"PAreload :::: {payload}")
    # user_id = payload['sub']
    # token_record = db.query(models.TokenTable).all()
    # info = []
    # for record in token_record:
    #     print("record", record)
    #     if (datetime.utcnow() - record.created_date).days > 1:
    #         info.append(record.user_id)
    # if info:
    #     existing_token = db.query(models.TokenTable).where(TokenTable.user_id.in_(info)).delete()
    #     db.commit()
    #
    # existing_token = db.query(models.TokenTable).filter(models.TokenTable.user_id == user_id,
    #                                                     models.TokenTable.access_toke == token).first()
    # if existing_token:
    #     existing_token.status = False
    #     db.add(existing_token)
    #     db.commit()
    #     db.refresh(existing_token)
    return {"message": "Logout Successfully"}
