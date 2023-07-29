from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class UserType_Base(BaseModel):
    user_type: str
    usage_limit_days: int = 1
    created_at: datetime


# Schema for User Type Creation
class User_TypeCreate(UserType_Base):
    user_type: str
    usage_limit_days: int
    created_at = datetime.now()


# Schema for User Type Retrieval
class User_Type(UserType_Base):
    id: int
    user_type: str
    usage_limit_days: int

    class Config:
        orm_mode = True


class User_TypeUpdate(UserType_Base):
    id: Optional[int] = None
    user_type: str
    usage_limit_days: int


class User_TypeInDBBase(UserType_Base):
    id: Optional[int] =  None
    user_type: str

    class Config:
        orm_mode = True


class User_Type(User_TypeInDBBase):
    pass

class User_TypeInDB(User_TypeInDBBase):
    user_type: str


