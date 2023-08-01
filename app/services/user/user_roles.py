from typing import Any, Optional

import sqlalchemy
from typing import Optional, Union, Dict, Any

from sqlalchemy.orm import Session
from app.models.user.user_roles import User_Roles
from app.schemas.user.user_roles import UserRole_Create, UserRole_Update
from app.services.base import BaseService
from sqlalchemy.exc import IntegrityError
from starlette.exceptions import HTTPException


class UserRoleService(BaseService[User_Roles, UserRole_Create, UserRole_Update]):
    def __init__(self, db_session: Session):
        super(UserRoleService, self).__init__(User_Roles, db_session)

    def get_by_role(self, role: str) -> Optional[User_Roles]:
        return self.db_session.query(User_Roles).filter(User_Roles.user_role == role).first()

    def create(self, obj_in: UserRole_Create) -> User_Roles:
        db_obj = User_Roles(
            user_role=obj_in.user_role,
            user_access_level=obj_in.user_access_level
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


# from typing import Optional, Union, Dict, Any
#
# import sqlalchemy
# from sqlalchemy.orm import Session
# from app.services.crud_base import CRUDBase
# from app.models.user.user_roles import User_Roles
# from app.schemas.user.user_roles import UserRole_Create, UserRole_Update
# from sqlalchemy.exc import IntegrityError
# from starlette.exceptions import HTTPException
#
#
# class CRUDUserRole(CRUDBase[User_Roles, UserRole_Create, UserRole_Update]):
#     def get_by_role(self, db: Session, *, role: str) -> Optional[User_Roles]:
#         return db.query(User_Roles).filter(User_Roles.user_role == role).first()
#
#     def create(self, db: Session, *, obj_in: UserRole_Create) -> User_Roles:
#         db_obj = User_Roles(
#             user_role=obj_in.user_role,
#             user_access_level=obj_in.user_access_level
#         )
#         try:
#             db.commit()
#         except sqlalchemy.exc.IntegrityError as e:
#             db.rollback()
#             if "duplicate key" in str(e):
#                 raise HTTPException(status_code=409, detail="Conflict Error")
#             else:
#                 raise e
#         return db_obj
#
#     def update(
#             self, db: Session, *, db_obj: User_Roles, obj_in: Union[UserRole_Update, Dict[str, Any]]
#     ) -> User_Roles:
#         if isinstance(obj_in, dict):
#             update_data = obj_in
#         else:
#             update_data = obj_in.dict(exclude_unset=True)
#         if update_data["user_access_level"]:
#             user_access_level = update_data["user_access_level"]
#             del update_data["user_access_level"]
#             update_data["user_access_level"] = user_access_level
#         return super().update(db, db_obj=db_obj, obj_in=update_data)
#
#
# user_role = CRUDUserRole(User_Roles)
