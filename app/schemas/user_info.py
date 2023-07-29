from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, condecimal
from app.schemas.schema_utils import to_camel
from app.schemas.user_roles import User_Role
from app.schemas.user_types import User_Type


class User_InfoBase(BaseModel):    
    user_id: str
    user_name: str
    user_email: EmailStr 
    user_mobile: str
    user_location: Optional[str]
    user_password: str
    user_role: int
    user_type: int
    user_credit: condecimal(decimal_places=2)
    user_is_deleted: bool
    user_is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


class User_InfoUpdate(User_InfoBase):
    user_name: Optional[str]
    user_location: Optional[str]
    user_password: Optional[str]
    user_role: Optional[int]
    user_type: Optional[int]
    user_credit: Optional[condecimal(decimal_places=2)]
    user_is_deleted: Optional[bool]
    user_is_active: Optional[bool]
    updated_at: datetime = datetime.now()
    

class User_InfoCreate(User_InfoBase):
    user_id: str
    user_name: str
    user_email: EmailStr 
    user_mobile: str
    user_location: Optional[str]
    user_password: str
    user_role: int
    user_type: int
    user_credit: condecimal(decimal_places=2)
    user_is_deleted: bool
    user_is_active: bool
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()


class User_Info(User_InfoBase):
    user_id: str
    user_name: str
    user_email: EmailStr 
    user_mobile: str
    user_location: Optional[str]
    user_password: str
    user_role: int
    user_type: int
    user_credit: condecimal(decimal_places=2)
    user_is_deleted: bool
    user_is_active: bool
    created_at: datetime
    updated_at: datetime
     
    class Config:
        orm_mode = True