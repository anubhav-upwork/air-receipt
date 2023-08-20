from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, condecimal
from app.schemas.schema_utils import to_camel


class UserLogin_Base(BaseModel):
    is_logged_in: bool

    class Config:
        alias_generator = to_camel
        populate_by_name = True


class UserLogin_Update(UserLogin_Base):
    user_id: int
    token: Optional[str]
    is_logged_in: Optional[bool]
    is_expired: Optional[bool]

    class Config:
        from_attributes = True


class UserLogin_Create(UserLogin_Base):
    user_id: int
    token: str
    is_logged_in: Optional[bool]
    is_expired: Optional[bool]

    class Config:
        from_attributes = True
        alias_generator = to_camel
        populate_by_name = True


class UserLogin(UserLogin_Base):
    user_id: int
    token: str
    is_logged_in: bool
    is_expired: bool
    created_at: datetime
    updated_at: datetime = None

    class Config:
        from_attributes = True
        alias_generator = to_camel
        populate_by_name = True
