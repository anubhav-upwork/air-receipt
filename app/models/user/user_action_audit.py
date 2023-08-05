import datetime
import enum
from sqlalchemy import Column, types, ForeignKey
from sqlalchemy.orm import relationship
from app.db.dbconnect import Base


class User_Action(str, enum.Enum):
    login = "LOGIN"
    logout = "LOGOUT"
    token_expire = "TOKEN_EXPIRE"
    token_request = "TOKEN_REQUEST"

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
