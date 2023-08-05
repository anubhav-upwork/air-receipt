from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.models.user.user_roles import User_Roles
from app.schemas.user.user_roles import UserRole, UserRole_Create, UserRole_Update
from app.services.user import get_user_role_service, UserRoleService

router = APIRouter(prefix="/roles", tags=["Role"])


@router.post("/create_role", status_code=201, response_model=UserRole)
async def create_role(role: UserRole_Create,
                      user_role_service: UserRoleService = Depends(get_user_role_service)) -> User_Roles:
    print("create : ", role)
    existing_role = user_role_service.get_by_role(role=role.user_role)
    if existing_role:
        raise HTTPException(
            status_code=400, detail="Role already exists"
        )
    return user_role_service.create(role)


@router.patch("/update_access_level", status_code=201, response_model=UserRole)
async def update_access_level(role: UserRole_Update,
                              user_role_service: UserRoleService = Depends(get_user_role_service)) -> User_Roles:
    print("update : ", role)
    existing_role = user_role_service.get_by_role(role=role.user_role)
    if not existing_role:
        raise HTTPException(
            status_code=400, detail="Role does not exist"
        )
    return user_role_service.update(existing_role.id, role)


@router.get("/", status_code=201, response_model=List[UserRole])
async def list_user_roles(user_roles_service: UserRoleService = Depends(get_user_role_service)) -> List[User_Roles]:
    return user_roles_service.list()


@router.delete("/{user_role}", status_code=201, response_model=UserRole)
async def delete_role(user_role: str, user_roles_service: UserRoleService = Depends(get_user_role_service)) -> User_Roles:
    existing_role = user_roles_service.get_by_role(role=user_role)
    if not existing_role:
        raise HTTPException(
            status_code=400, detail="Role does not exist"
        )
    return user_roles_service.delete(existing_role.id)

