from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.models.user.user_types import User_Types
from app.schemas.user.user_types import UserType, UserType_Create, UserType_Update
from app.services.user import get_user_type_service, UserTypeService

router = APIRouter(prefix="/user_types")


@router.post("/create_type", status_code=201, response_model=UserType)
async def create_role(utype: UserType_Create,
                      user_type_service: UserTypeService = Depends(get_user_type_service)) -> User_Types:
    existing_type = user_type_service.get_by_type(utype=utype.user_type)
    if existing_type:
        raise HTTPException(
            status_code=400, detail="User Type already exists"
        )
    return user_type_service.create(utype)


@router.patch("/update_usage_limit", status_code=201, response_model=UserType)
async def update_access_level(user_type: UserType_Update,
                              user_type_service: UserTypeService = Depends(get_user_type_service)) -> User_Types:
    existing_type = user_type_service.get_by_type(utype=user_type.user_type)
    if not existing_type:
        raise HTTPException(
            status_code=400, detail="User Type does not exists"
        )
    return user_type_service.update(existing_type.id, user_type)


@router.get("/", status_code=201, response_model=List[UserType])
async def list_orders(user_type_service: UserTypeService = Depends(get_user_type_service)) -> List[User_Types]:
    return user_type_service.list()


@router.delete("/{user_type}", status_code=201, response_model=UserType)
async def delete_role(user_type: str,
                      user_type_service: UserTypeService = Depends(get_user_type_service)) -> User_Types:
    existing_type = user_type_service.get_by_type(utype=user_type)
    if not existing_type:
        raise HTTPException(
            status_code=400, detail="User Type does not exist"
        )
    return user_type_service.delete(existing_type.id)
