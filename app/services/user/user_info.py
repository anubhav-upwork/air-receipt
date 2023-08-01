from typing import Any, Optional

import sqlalchemy
from typing import Optional, Union, Dict, Any

from sqlalchemy.orm import Session
from app.models.user.user_info import User_Info
from app.schemas.user.user_info import UserInfo_Create, UserInfo_Update
from app.services.base import BaseService
from sqlalchemy.exc import IntegrityError
from starlette.exceptions import HTTPException
from app.api.security import hash_password, validate_password


class UserInfoService(BaseService[User_Info, UserInfo_Create, UserInfo_Update]):
    def __init__(self, db_session: Session):
        super(UserInfoService, self).__init__(User_Info, db_session)

    def get_by_email(self, uemail: str) -> Optional[User_Info]:
        return self.db_session.query(User_Info).filter(User_Info.user_email == uemail).first()

    def get_by_mobile(self, umobile: str) -> Optional[User_Info]:
        return self.db_session.query(User_Info).filter(User_Info.user_mobile == umobile).first()

    def get_credit(self, uemail: str) -> Optional[User_Info.user_credit]:
        return self.db_session.query(User_Info).filter(User_Info.user_email == uemail).first().user_credit

    def create(self, obj_in: UserInfo_Create) -> User_Info:
        db_obj = User_Info(
            user_name=obj_in.user_name,
            user_email=obj_in.user_email,
            user_mobile=obj_in.user_mobile,
            user_location=obj_in.user_location,
            user_password=hash_password(obj_in.user_password),
            user_role=obj_in.user_role,
            user_type=obj_in.user_type,
            user_credit=obj_in.user_credit,
            user_is_deleted=False,
            user_is_active=True
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

    def authenticate(self, email: str, password: str) -> Optional[User_Info]:
        user = self.get_by_email(uemail=email)
        if not user:
            return None
        if not validate_password(password, user.hashed_password):
            return None
        return user
