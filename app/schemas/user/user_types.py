from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.schemas.schema_utils import to_camel


# Schema of User Type Base Class
class UserType_Base(BaseModel):
    user_type: str
    usage_limit_days: int
    # created_at: datetime

    class Config:
        alias_generator = to_camel
        populate_by_name = True


# Schema for Update of User_Type
class UserType_Update(UserType_Base):
    user_type: Optional[str]
    usage_limit_days: int


# Schema for User Type Creation
class UserType_Create(UserType_Base):
    user_type: str
    usage_limit_days: int = 1
    # created_at: datetime = datetime.now()


# Schema for User Type Retrieval
class UserType(UserType_Base):
    id: int
    user_type: str
    usage_limit_days: int
    created_at: datetime

    class Config:
        from_attributes = True
