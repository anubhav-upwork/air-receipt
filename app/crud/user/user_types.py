from typing import Any, Optional
import sqlalchemy
from typing import Optional, Union, Dict, Any

from sqlalchemy.orm import Session
from app.models.user.user_types import User_Types
from app.schemas.user.user_types import UserType_Create, UserType_Update
from app.crud.base import BaseService
from sqlalchemy.exc import IntegrityError
from starlette.exceptions import HTTPException


class UserTypeService(BaseService[User_Types, UserType_Create, UserType_Update]):

    def get_by_type(self, db_session: Session, utype: str) -> Optional[User_Types]:
        return db_session.query(User_Types).filter(User_Types.user_type == utype).first()

    def create(self, db_session: Session, obj_in: UserType_Create) -> User_Types:
        db_obj = User_Types(
            user_type=obj_in.user_type,
            usage_limit_days=obj_in.usage_limit_days
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


get_user_type_service = UserTypeService(User_Types)
