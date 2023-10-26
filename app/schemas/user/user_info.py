from datetime import datetime
from typing import Optional
from pydantic import BaseModel, condecimal, EmailStr
from app.schemas.schema_utils import to_camel


class UserInfo_Base(BaseModel):
    class Config:
        alias_generator = to_camel
        populate_by_name = True


# write only those that are required to be filled up while the rows are updated
class UserInfo_Update(UserInfo_Base):
    user_name: Optional[str] = None
    user_mobile: Optional[str] = None
    user_location: Optional[str] = None
    user_password: Optional[str] = None
    user_role: Optional[int] = None
    user_type: Optional[int] = None
    user_credit: Optional[condecimal(decimal_places=2)] = None
    user_is_deleted: Optional[bool] = None
    user_is_active: Optional[bool] = None

    class Config:
        from_attributes = True


class UserInfo_Create(UserInfo_Base):
    user_name: str = "user_name"
    user_email: EmailStr = "user@example.com"
    user_mobile: str = "91890890"
    user_location: Optional[str] = "Sydney,Australia"
    user_password: str
    user_role: int = 1
    user_type: int = 1
    user_credit: condecimal(decimal_places=2) = 1.00  # Adding 1 credit for basic trial
    user_is_deleted: bool = False
    user_is_active: bool = True

    class Config:
        from_attributes = True
        alias_generator = to_camel
        populate_by_name = True


# Super User Row Pydantic
class UserInfoSuper_Create(UserInfo_Base):
    user_name: str
    user_email: EmailStr
    user_mobile: str
    user_location: Optional[str] = None
    user_password: str
    user_role: int
    user_type: int
    user_credit: condecimal(decimal_places=2)
    user_is_deleted: bool
    user_is_active: bool = True
    user_is_superuser: bool = False

    class Config:
        from_attributes = True
        alias_generator = to_camel
        populate_by_name = True


class UserInfoShare(UserInfo_Base):
    user_name: str
    user_email: str
    user_mobile: str
    user_role: int
    user_type: int

    class Config:
        from_attributes = True
        alias_generator = to_camel
        populate_by_name = True


# Response Pydantic schema -- Show everything except password
class UserInfo(UserInfo_Base):
    id: int
    user_name: str
    user_email: EmailStr
    user_mobile: str
    user_location: Optional[str] = None
    user_password: str
    user_role: int
    user_type: int
    user_credit: condecimal(decimal_places=2)
    user_is_deleted: bool
    user_is_active: bool
    user_is_superuser: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        alias_generator = to_camel
        populate_by_name = True
