from typing import Any

from sqlalchemy.orm import Session

from app.models.user.user_types import User_Types
from app.schemas.user.user_types import UserType_Create, UserType_Update

from app.services.base import BaseService


class UserRole_Service(BaseService[User_Types, UserType_Create, UserType_Update]):

    def __init__(self, db_session: Session):
        super(UserRole_Service, self).__init__(User_Types, db_session)
