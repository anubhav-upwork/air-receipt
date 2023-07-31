from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# from app.db.dbconnect import get_session
from app.models.user.user_roles import User_Roles
from app.schemas.user.user_roles import UserRole, UserRole_Create, UserRole_Update
from app.services.user import get_user_role_service, UserRoleService


router = APIRouter(prefix="/roles")


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


# @router.post("/login", response_model=schemas.Token)
# def login(user_login: schemas.UserLogin, db: Session = Depends(get_db)):
#     access_token = services.authenticate_user(db, user_login)
#
#     if access_token is None:
#         raise HTTPException(status_code=400, detail="Invalid email or password")
#     return {"access_token": access_token, "token_type": "Bearer"}
