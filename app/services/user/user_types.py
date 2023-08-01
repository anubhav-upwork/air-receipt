from typing import Any, Optional
import sqlalchemy
from typing import Optional, Union, Dict, Any

from sqlalchemy.orm import Session
from app.models.user.user_types import User_Types
from app.schemas.user.user_types import UserType_Create, UserType_Update
from app.services.base import BaseService
from sqlalchemy.exc import IntegrityError
from starlette.exceptions import HTTPException


class UserTypeService(BaseService[User_Types, UserType_Create, UserType_Update]):
    def __init__(self, db_session: Session):
        super(UserTypeService, self).__init__(User_Types, db_session)

    def get_by_type(self, utype: str) -> Optional[User_Types]:
        return self.db_session.query(User_Types).filter(User_Types.user_type == utype).first()

    def create(self, obj_in: UserType_Create) -> User_Types:
        db_obj = User_Types(
            user_type=obj_in.user_type,
            usage_limit_days=obj_in.usage_limit_days
        )
        self.db_session.add(db_obj)
        try:
            self.db_session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            self.db_session.rollback()
            if "duplicate key" in str(e):
                raise HTTPException(status_code=409, detail="Conflict Error")
            else:
                raise e
        self.db_session.refresh(db_obj)
        return db_obj
