from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.schemas.schema_utils import to_camel


class UserLogin_Base(BaseModel):
    status: bool

    class Config:
        alias_generator = to_camel
        populate_by_name = True


class UserLogin_Update(UserLogin_Base):
    access_token: Optional[str]
    refresh_token: Optional[str]
    status: bool


class UserLogin_Create(UserLogin_Base):
    user_id: int
    access_token: str
    refresh_token: str
    status: bool

    class Config:
        from_attributes = True
        alias_generator = to_camel
        populate_by_name = True


class UserLogin(UserLogin_Base):
    user_id: int
    access_token: str
    refresh_token: str
    status: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        alias_generator = to_camel
        populate_by_name = True
