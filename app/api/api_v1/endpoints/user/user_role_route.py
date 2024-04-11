from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api import deps
from app.core.http_exceptions import DuplicateValueException, UnauthorizedException, NotFoundException
from app.crud.user.user_roles import get_user_role_service
from app.models.user.user_info import User_Info
from app.models.user.user_roles import User_Roles
from app.schemas.user.user_roles import UserRole, UserRole_Create, UserRole_Update

router = APIRouter(prefix="/roles", tags=["Role"])


@router.post("/create_role", status_code=status.HTTP_201_CREATED, response_model=UserRole)
async def create_role(role: UserRole_Create,
                      db: Session = Depends(deps.get_db),
                      cur_user: User_Info = Depends(deps.get_current_user)) -> User_Roles:
    if not cur_user.user_is_superuser:
        raise UnauthorizedException("Not authorized to access this, Only SuperUser can access")

    existing_role = get_user_role_service.get_by_role(db_session=db, role=role.user_role)
    if existing_role:
        raise DuplicateValueException("Role already exists")

    return get_user_role_service.create(db_session=db, obj_in=role)


@router.patch("/update_access_level", status_code=status.HTTP_201_CREATED, response_model=UserRole)
async def update_access_level(role: UserRole_Update,
                              db: Session = Depends(deps.get_db),
                              cur_user: User_Info = Depends(deps.get_current_user)) -> User_Roles:
    if not cur_user.user_is_superuser:
        raise UnauthorizedException("Not authorized to access this, Only SuperUser can access")

    existing_role = get_user_role_service.get_by_role(db_session=db, role=role.user_role)
    if not existing_role:
        raise NotFoundException("Role does not exist")

    return get_user_role_service.update(db_session=db, _id=existing_role.id, obj=role)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[UserRole])
async def list_user_roles(db: Session = Depends(deps.get_db),
                          cur_user: User_Info = Depends(deps.get_current_user)) -> List[User_Roles]:
    if not cur_user.user_is_superuser:
        return get_user_role_service.list(db_session=db).remove(UserRole(user_role="superadmin"))
    return get_user_role_service.list(db_session=db)


@router.delete("/{user_role}", status_code=status.HTTP_201_CREATED, response_model=UserRole)
async def delete_role(user_role: str,
                      db: Session = Depends(deps.get_db),
                      cur_user: User_Info = Depends(deps.get_current_user)) -> User_Roles:
    if not cur_user.user_is_superuser:
        raise UnauthorizedException("Not authorized to access this, Only SuperUser can access")

    existing_role = get_user_role_service.get_by_role(db_session=db, role=user_role)
    if not existing_role:
        raise NotFoundException("Role does not exist")

    return get_user_role_service.delete(db_session=db, _id=existing_role.id)
