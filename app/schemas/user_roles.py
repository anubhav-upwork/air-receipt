from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class UserRole_Base(BaseModel):
    user_role: Optional[str] = None
    created_at: Optional[datetime]

# Schema for User Role Creation
class User_RoleCreate(UserRole_Base):
    user_role: str
    created_at = datetime.now()
    
# Schema for User Role Retrieval
class User_RoleResponse(UserRole_Base):
    id: int
    user_role: str
    created_at: datetime

    class Config:
        orm_mode=True

