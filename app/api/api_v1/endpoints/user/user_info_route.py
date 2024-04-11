from typing import List
from pydantic import EmailStr
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from app.core.http_exceptions import UnauthorizedException
from app.models.user.user_info import User_Info
from app.schemas.user.user_info import UserInfo, UserInfo_Create, UserInfo_Update, UserInfoShare
from app.crud.user.user_info import get_user_info_service
from app.api import deps
from app.core.security import hash_password

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[UserInfo])
async def list_users(db: Session = Depends(deps.get_db),
                     cur_user: User_Info = Depends(deps.get_current_user)) -> List[User_Info]:
    if not cur_user.user_is_superuser:
        raise UnauthorizedException("Not authorized to access this, Only SuperUser can access")
    return get_user_info_service.list(db_session=db)


@router.patch("/update_user", status_code=status.HTTP_201_CREATED, response_model=UserInfo_Update)
async def update_user(email: EmailStr, uinfo: UserInfo_Update,
                      db: Session = Depends(deps.get_db),
                      cur_user: User_Info = Depends(deps.get_current_user)) -> User_Info:
    existing_user_email = get_user_info_service.get_by_email(db_session=db, uemail=email)
    if not existing_user_email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User {email}does not exist"
        )

    if cur_user.user_email != email:
        raise UnauthorizedException("Not authorized to access this")
    elif not cur_user.user_is_superuser:
        raise UnauthorizedException("Not authorized to access this")
    else:
        return get_user_info_service.update(db_session=db, _id=existing_user_email.id, obj=uinfo)


@router.get("/check_email_exists/{email}", status_code=status.HTTP_200_OK, response_model=str)
async def check_email_exists(email: EmailStr,
                             db: Session = Depends(deps.get_db)) -> str:
    existing_user_email = get_user_info_service.get_by_email(db_session=db, uemail=email)
    if not existing_user_email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {email} does not exist"
        )
    return f"User {email} exists"


@router.get("/get_userinfo_email/{email}", status_code=status.HTTP_200_OK, response_model=UserInfoShare)
async def get_userinfo_email(email: EmailStr,
                             db: Session = Depends(deps.get_db)) -> User_Info:
    existing_user_email = get_user_info_service.get_by_email(db_session=db, uemail=email)
    if not existing_user_email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {email} does not exist"
        )
    return existing_user_email


@router.get("/check_user_exists/{user_name}", status_code=status.HTTP_200_OK, response_model=str)
async def check_user_exists(user_name: str,
                            db: Session = Depends(deps.get_db)) -> str:
    existing_user = get_user_info_service.get_by_usr(db_session=db, usr=user_name)
    if not existing_user:
        raise HTTPException(
            status_code=404, detail=f"User with {user_name} does not exist"
        )
    return f"User {user_name} exists"


@router.patch("/update_user_password", status_code=status.HTTP_201_CREATED, response_model=UserInfo_Update)
async def update_user_password(email: EmailStr,
                               phone: str,
                               password: str,
                               db: Session = Depends(deps.get_db),
                               cur_user: User_Info = Depends(deps.get_current_user)) -> User_Info:
    if cur_user.user_email != email:
        raise UnauthorizedException("Not authorized to access this")
    elif not cur_user.user_is_superuser:
        raise UnauthorizedException("Not authorized to access this")
    else:
        existing_user_email = get_user_info_service.get_by_email(db_session=db, uemail=email)
        if not existing_user_email or (existing_user_email.user_mobile != phone):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"User {email} does not exist"
            )

        uinfo = UserInfo_Update(
            user_password=hash_password(password)
        )
        return get_user_info_service.update(db_session=db, _id=existing_user_email.id, obj=uinfo)


@router.patch("/forget_password", status_code=status.HTTP_201_CREATED)
async def forget_password(email: EmailStr,
                          db: Session = Depends(deps.get_db)):
    existing_user_email = get_user_info_service.get_by_email(db_session=db, uemail=email)
    if not existing_user_email:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User {email} does not exist"
        )
    return {"response": "Your request to reset password is sent to your inbox"}
