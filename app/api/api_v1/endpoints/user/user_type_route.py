from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.user.user_types import User_Types
from app.schemas.user.user_types import UserType, UserType_Create, UserType_Update
from app.crud.user.user_types import get_user_type_service
from app.api import deps

router = APIRouter(prefix="/user_types", tags=["Type"])


@router.post("/create_type", status_code=201, response_model=UserType)
async def create_type(utype: UserType_Create,
                      db: Session = Depends(deps.get_db)) -> User_Types:
    existing_type = get_user_type_service.get_by_type(db_session=db, utype=utype.user_type)
    if existing_type:
        raise HTTPException(
            status_code=400, detail="User Type already exists"
        )
    return get_user_type_service.create(db_session=db, obj_in=utype)


@router.patch("/update_usage_limit", status_code=201, response_model=UserType)
async def update_usage_limit(user_type: UserType_Update,
                             db: Session = Depends(deps.get_db)) -> User_Types:
    existing_type = get_user_type_service.get_by_type(db_session=db, utype=user_type.user_type)
    if not existing_type:
        raise HTTPException(
            status_code=400, detail="User Type does not exists"
        )
    return get_user_type_service.update(db_session=db, _id=existing_type.id, obj=user_type)


@router.get("/", status_code=201, response_model=List[UserType])
async def list_user_types( db: Session = Depends(deps.get_db)) -> List[User_Types]:
    return get_user_type_service.list(db_session=db)


@router.delete("/{user_type}", status_code=201, response_model=UserType)
async def delete_type(user_type: str,
                      db: Session = Depends(deps.get_db)) -> User_Types:
    existing_type = get_user_type_service.get_by_type(db_session=db, utype=user_type)
    if not existing_type:
        raise HTTPException(
            status_code=400, detail="User Type does not exist"
        )
    return get_user_type_service.delete(db_session=db, _id=existing_type.id)
