from pydantic import BaseModel, EmailStr


# Schema for User Role Creation
class User_RoleCreate(BaseModel):
    user_role: str


# Schema for User Role Retrieval
class User_RoleResponse(User_RoleCreate):
    id: int
    user_role: str

    class Config:
        from_attributes = True
