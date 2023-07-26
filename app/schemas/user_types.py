from pydantic import BaseModel, EmailStr


# Schema for User Type Creation
class User_TypeCreate(BaseModel):
    user_type: str
    usage_limit_days: int


# Schema for User Type Retrieval
class User_TypeResponse(User_TypeCreate):
    id: int
    user_type: str
    usage_limit_days: int

    class Config:
        from_attributes = True


class User_TypeUpdate(User_TypeCreate):
    usage_limit_days: int
