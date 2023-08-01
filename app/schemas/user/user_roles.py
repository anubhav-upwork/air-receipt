from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.schemas.schema_utils import to_camel


# Schema of User Role Base Class
class UserRole_Base(BaseModel):
    user_role: str
    user_access_level: int
    # created_at: datetime

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


# Schema for Update of User_Role
class UserRole_Update(UserRole_Base):
    id: Optional[int]
    user_role: Optional[str]
    user_access_level: int


# Schema for User Role Creation
class UserRole_Create(UserRole_Base):
    user_role: str
    user_access_level: int = -1
    # created_at = datetime.now()


# Schema for User Role Retrieval
class UserRole(UserRole_Base):
    id: int
    user_role: str
    user_access_level: int
    created_at: datetime

    class Config:
        orm_mode = True
