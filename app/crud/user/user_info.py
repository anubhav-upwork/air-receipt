from typing import Optional

import sqlalchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException

from app.core.security import hash_password, validate_password
from app.crud.base import BaseService
from app.models.user.user_info import User_Info
from app.schemas.user.user_info import UserInfo_Create, UserInfoSuper_Create, UserInfo_Update


class UserInfoService(BaseService[User_Info, UserInfo_Create, UserInfo_Update]):

    def get_by_email(self, db_session: Session, uemail: str) -> Optional[User_Info]:
        return db_session.query(User_Info).filter(User_Info.user_email == uemail).first()

    def get_by_usr(self, db_session: Session, usr: str) -> Optional[User_Info]:
        return db_session.query(User_Info).filter(User_Info.user_name == usr).first()

    def get_by_mobile(self, db_session: Session, umobile: str) -> Optional[User_Info]:
        return db_session.query(User_Info).filter(User_Info.user_mobile == umobile).first()

    def get_by_uid(self, db_session: Session, uid: int) -> Optional[User_Info]:
        return db_session.query(User_Info).filter(User_Info.id == uid).first()

    def get_credit(self, db_session: Session, uemail: str) -> float:
        return db_session.query(User_Info).filter(User_Info.user_email == uemail).first().user_credit

    def is_superuser(self, user: User_Info) -> bool:
        return user.user_is_superuser

    def create(self, db_session: Session, obj_in: UserInfo_Create) -> User_Info:
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

    def create_super_user(self, db_session: Session, obj_in: UserInfoSuper_Create) -> User_Info:
        db_obj = User_Info(
            user_name=obj_in.user_name,
            user_email=obj_in.user_email,
            user_mobile=obj_in.user_mobile,
            user_location=obj_in.user_location,
            user_password=hash_password(obj_in.user_password),
            user_role=obj_in.user_role,
            user_type=obj_in.user_type,
            user_credit=obj_in.user_credit,
            user_is_superuser=obj_in.user_is_superuser,
            user_is_deleted=False,
            user_is_active=True
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

    def authenticate(self, db_session: Session, email: str, password: str) -> Optional[User_Info]:
        user = self.get_by_email(db_session=db_session, uemail=email)
        if not user:
            return None
        if not validate_password(password, user.hashed_password):
            return None
        return user


get_user_info_service = UserInfoService(User_Info)

