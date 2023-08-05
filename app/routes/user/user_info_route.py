from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.models.user.user_info import User_Info
from app.schemas.user.user_info import UserInfo, UserInfo_Create, UserInfo_Update
from app.services.user import get_user_info_service, UserInfoService

router = APIRouter(prefix="/user", tags=["User"])


@router.post("/create_user", status_code=201, response_model=UserInfo)
async def create_user(uinfo: UserInfo_Create,
                      user_info_service: UserInfoService = Depends(get_user_info_service)) -> User_Info:
    existing_user_email = user_info_service.get_by_email(uemail=uinfo.user_email)
    existing_user_mobile = user_info_service.get_by_mobile(umobile=uinfo.user_mobile)
    if existing_user_email or existing_user_mobile:
        raise HTTPException(
            status_code=400, detail="User already exists"
        )
    return user_info_service.create(uinfo)


@router.get("/", status_code=201, response_model=List[UserInfo])
async def list_users(user_info_service: UserInfoService = Depends(get_user_info_service)) -> List[User_Info]:
    return user_info_service.list()


@router.patch("/update_user", status_code=201, response_model=UserInfo_Update)
async def update_user(uinfo: UserInfo_Update,
                      user_info_service: UserInfoService = Depends(get_user_info_service)) -> User_Info:
    existing_user_email = user_info_service.get_by_email(uemail=uinfo.user_email)
    if not existing_user_email:
        raise HTTPException(
            status_code=400, detail="User does not exist"
        )
    return user_info_service.update(existing_user_email.id, uinfo)
