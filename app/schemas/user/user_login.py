# from datetime import datetime
# from typing import Optional
# from pydantic import BaseModel, EmailStr, condecimal
# from app.schemas.schema_utils import to_camel
#
#
# class UserLogin_Base(BaseModel):
#
#     user_is_deleted: bool
#     user_is_active: bool
#
#     class Config:
#         alias_generator = to_camel
#         allow_population_by_field_name = True
#
#
# class UserLogin_Update(UserLogin_Base):
#     user_name: Optional[str]
#     user_mobile: Optional[str]
#     user_location: Optional[str]
#     user_password: Optional[str]
#     user_role: Optional[int]
#     user_type: Optional[int]
#     user_credit: Optional[condecimal(decimal_places=2)]
#     user_is_deleted: Optional[bool]
#     user_is_active: Optional[bool]
#
#     class Config:
#         orm_mode = True
#
#
# class UserLogin_Create(UserLogin_Base):
#     user_id: str
#     user_email: EmailStr
#     user_mobile: str
#     user_location: Optional[str]
#     user_password: str
#     user_role: int
#     user_type: int
#     user_credit: condecimal(decimal_places=2)
#     user_is_deleted: bool = False
#     user_is_active: bool = True
#
#     # created_at: datetime = datetime.now()
#     # updated_at: datetime = datetime.now()
#
#     class Config:
#         orm_mode = True
#         alias_generator = to_camel
#         allow_population_by_field_name = True
#
#
# class UserLogin(UserLogin_Base):
#     id: int
#     user_id: int
#     token: str
#     is_logged_in: bool
#     is_expired: bool
#     created_at: datetime
#     updated_at: datetime = None
#
#     class Config:
#         orm_mode = True
#         alias_generator = to_camel
#         allow_population_by_field_name = True
