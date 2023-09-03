from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from app.schemas.schema_utils import to_camel


# Schema of User Role Base Class
class UserRole_Base(BaseModel):
    user_role: str = Field(..., min_length=1, max_length=50, examples=["superadmin", "admin", "tenant", "reviewer"])
    user_access_level: int

    class Config:
        alias_generator = to_camel
        populate_by_name = True


# Schema for Update of User_Role
class UserRole_Update(UserRole_Base):
    id: Optional[int]
    user_role: Optional[str]
    user_access_level: int


# Schema for User Role Creation
class UserRole_Create(UserRole_Base):
    user_role: str
    user_access_level: int = -1


# Schema for User Role Retrieval/Response
class UserRole(UserRole_Base):
    id: int = Field(...)
    user_role: str
    user_access_level: int
    created_at: datetime

    class Config:
        from_attributes = True
