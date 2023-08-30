from typing import List
from pydantic import EmailStr
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status
from app.models.user.user_info import User_Info
from app.schemas.user.user_info import UserInfo, UserInfo_Create, UserInfo_Update
from app.crud.user.user_info import get_user_info_service
from app.api import deps

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/create_user", status_code=status.HTTP_201_CREATED, response_model=UserInfo)
async def create_user(uinfo: UserInfo_Create,
                      db: Session = Depends(deps.get_db)) -> User_Info:
    existing_user_email = get_user_info_service.get_by_email(db_session=db, uemail=uinfo.user_email)
    existing_user_mobile = get_user_info_service.get_by_mobile(db_session=db, umobile=uinfo.user_mobile)
    if existing_user_email or existing_user_mobile:
        raise HTTPException(
            status_code=400, detail="User already exists"
        )
    return get_user_info_service.create(db_session=db, obj_in=uinfo)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[UserInfo])
async def list_users(db: Session = Depends(deps.get_db)) -> List[User_Info]:
    return get_user_info_service.list(db_session=db)


@router.patch("/update_user", status_code=status.HTTP_201_CREATED, response_model=UserInfo_Update)
async def update_user(email: EmailStr, uinfo: UserInfo_Update,
                      db: Session = Depends(deps.get_db)) -> User_Info:
    existing_user_email = get_user_info_service.get_by_email(db_session=db, uemail=email)
    if not existing_user_email:
        raise HTTPException(
            status_code=400, detail="User does not exist"
        )
    return get_user_info_service.update(db_session=db, _id=existing_user_email.id, obj=uinfo)
