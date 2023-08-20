import datetime
import enum
from sqlalchemy import Column, types, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class User_Action(str, enum.Enum):
    login = "LOGIN"
    logout = "LOGOUT"
    update = "UPDATE_INFO"
    credit_load = "CREDIT_LOAD"
    credit_payout = "CREDIT_PAYOUT"
    doc_upload = "DOC_UPLOAD"
    doc_review = "DOC_REVIEW"
    doc_delete = "DOC_DELETE"


class User_Audit_Trail(Base):
    __tablename__ = "user_audit_trail"
    id = Column(types.Integer, primary_key=True)
    user_id = Column(types.Integer, ForeignKey('user_info.id'), nullable=False)
    action = Column(types.Enum(User_Action), nullable=False)
    action_msg = Column(types.String(250), nullable=True)
    created_at = Column(types.DateTime, nullable=False, default=datetime.datetime.now())
