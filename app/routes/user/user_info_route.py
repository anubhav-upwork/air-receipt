from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.models.user.user_info import User_Info
from app.schemas.user.user_info import UserInfo, UserInfo_Create, UserInfo_Update
from app.services.user import get_user_info_service, UserInfoService

router = APIRouter(prefix="/user")


@router.post("/create_user", status_code=201, response_model=UserInfo)
async def create_role(uinfo: UserInfo_Create,
                      user_info_service: UserInfoService = Depends(get_user_info_service)) -> User_Info:
    existing_user_email = user_info_service.get_by_email(uemail=uinfo.user_email)
    existing_user_mobile = user_info_service.get_by_mobile(umobile=uinfo.user_mobile)
    if existing_user_email or existing_user_mobile:
        raise HTTPException(
            status_code=400, detail="User already exists"
        )
    return user_info_service.create(uinfo)
