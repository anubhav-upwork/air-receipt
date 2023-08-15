from datetime import datetime
from typing import Optional
from pydantic import BaseModel, condecimal, EmailStr
from app.schemas.schema_utils import to_camel
from app.schemas.user.user_roles import UserRole, UserRole_Base
from app.schemas.user.user_types import UserType


class UserInfo_Base(BaseModel):
    user_name: str
    user_email: EmailStr
    user_mobile: str
    user_location: Optional[str]
    user_password: str
    user_role: int
    user_type: int
    user_credit: condecimal(decimal_places=2)
    user_is_deleted: bool
    user_is_active: bool

    class Config:
        alias_generator = to_camel
        populate_by_name = True


class UserInfo_Update(UserInfo_Base):
    user_name: Optional[str]
    user_mobile: Optional[str]
    user_location: Optional[str]
    user_password: Optional[str]
    user_role: Optional[int]
    user_type: Optional[int]
    user_credit: Optional[condecimal(decimal_places=2)]
    user_is_deleted: Optional[bool]
    user_is_active: Optional[bool]

    class Config:
        from_attributes = True


class UserInfo_Create(UserInfo_Base):
    user_name: str = "user_name"
    user_email: EmailStr = "user@example.com"
    user_mobile: str = "91890890"
    user_location: Optional[str]
    user_password: str
    user_role: int = 1
    user_type: int = 1
    user_credit: condecimal(decimal_places=2) = 1.00
    user_is_deleted: bool = False
    user_is_active: bool = True

    # created_at: datetime = datetime.now()
    # updated_at: datetime = datetime.now()

    class Config:
        from_attributes = True
        alias_generator = to_camel
        populate_by_name = True


class UserInfoSuper_Create(UserInfo_Base):
    user_is_superuser: bool = False

    class Config:
        from_attributes = True
        alias_generator = to_camel
        populate_by_name = True


class UserInfo(UserInfo_Base):
    id: int
    user_name: str
    user_email: EmailStr
    user_mobile: str
    user_location: Optional[str]
    user_password: str
    user_role: int
    user_type: int
    user_credit: condecimal(decimal_places=2)
    user_is_deleted: bool
    user_is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        alias_generator = to_camel
        populate_by_name = True
