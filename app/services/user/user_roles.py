from typing import Any

from sqlalchemy.orm import Session

from app.models.user.user_roles import User_Roles
from app.schemas.user.user_roles import UserRole_Create, UserRole_Update

from app.services.base import BaseService


class UserRole_Service(BaseService[User_Roles, UserRole_Create, UserRole_Update]):

    def __init__(self, db_session: Session):
        super(UserRole_Service, self).__init__(User_Roles, db_session)
