from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.models.user.user_action_audit import User_Action
from app.schemas.schema_utils import to_camel


# Schema of UserAuditTrail Base Class
class UserAuditTrail_Base(BaseModel):
    user_id: int

    class Config:
        alias_generator = to_camel
        populate_by_name = True


# Schema for Update of UserAuditTrail
class UserAuditTrail_Update(UserAuditTrail_Base):
    id: int
    user_id: int
    action: User_Action
    action_msg: Optional[str]


# Schema for UserAuditTrail Creation
class UserAuditTrail_Create(UserAuditTrail_Base):
    user_id: int
    action: User_Action
    action_msg: str


# Schema for UserAuditTrail Retrieval
class UserAuditTrail(BaseModel):
    id: int
    user_id: int
    action: User_Action
    action_msg: str
    created_at: datetime

    class Config:
        from_attributes = True
