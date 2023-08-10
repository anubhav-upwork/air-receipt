from typing import Any, Optional

import sqlalchemy
from typing import Optional, Union, Dict, Any

from sqlalchemy.orm import Session
from app.models.user.user_roles import User_Roles
from app.schemas.user.user_roles import UserRole_Create, UserRole_Update
from app.crud.base import BaseService
from sqlalchemy.exc import IntegrityError
from starlette.exceptions import HTTPException


class UserRoleService(BaseService[User_Roles, UserRole_Create, UserRole_Update]):

    def get_by_role(self, db_session: Session, role: str) -> Optional[User_Roles]:
        return db_session.query(User_Roles).filter(User_Roles.user_role == role).first()

    def create(self, db_session: Session, obj_in: UserRole_Create) -> User_Roles:
        db_obj = User_Roles(
            user_role=obj_in.user_role,
            user_access_level=obj_in.user_access_level
        )
        db_session.add(db_obj)
        try:
            db_session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            db_session.rollback()
            if "duplicate key" in str(e):
                raise HTTPException(status_code=409, detail="Conflict Error")
            else:
                raise e
        db_session.refresh(db_obj)
        return db_obj


userRoleCrud = UserRoleService(User_Roles)

