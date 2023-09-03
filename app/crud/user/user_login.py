from typing import Optional

import sqlalchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException

from app.crud.base import BaseService
from app.models.user.user_login import User_Login
from app.schemas.user.user_login import UserLogin_Create, UserLogin_Update


class UserLoginService(BaseService[User_Login, UserLogin_Create, UserLogin_Update]):

    def get_by_user_id(self, db_session: Session, user_id: int) -> Optional[User_Login]:
        return db_session.query(User_Login).filter(User_Login.user_id == user_id).first()

    # def get_by_mobile(self, db_session: Session, umobile: str) -> Optional[User_Info]:
    #     return db_session.query(User_Info).filter(User_Info.user_mobile == umobile).first()
    #
    # def get_credit(self, db_session: Session, uemail: str) -> float:
    #     return db_session.query(User_Info).filter(User_Info.user_email == uemail).first().user_credit
    #
    # def is_superuser(self, user: User_Info) -> bool:
    #     return user.user_is_superuser

    def create(self, db_session: Session, obj_in: UserLogin_Create) -> User_Login:
        db_obj = User_Login(
            user_id=obj_in.user_id,
            access_token=obj_in.access_token,
            refresh_token=obj_in.refresh_token,
            status=True
        )
        db_session.add(db_obj)
        try:
            db_session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            db_session.rollback()
            if "duplicate key" in str(e):
                raise HTTPException(status_code=409, detail="User Loging --- Conflict Error")
            else:
                raise e
        db_session.refresh(db_obj)
        return db_obj


get_user_login_service = UserLoginService(User_Login)
