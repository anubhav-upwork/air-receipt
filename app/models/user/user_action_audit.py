import datetime
import enum
from sqlalchemy import Column, types, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from app.db.dbconnect import Base

class User_Action_Audit(str, enum.Enum):
    login = "LOGIN"
    logout = "LOGOUT"
    token_expire = "TOKEN_EXPIRE"
    token_request = "TOKEN_REQUEST"
    
    doc_upload = "DOC_UPLOAD"
    doc_review = "DOC_REVIEW"
    doc_delete = "DOC_DELETE"
    

class Audit_Trail(Base):
    __tablename__ = "user_action_audit"
    id = Column(types.Integer, primary_key=True)
    user_id = Column(types.Integer, ForeignKey('user_info.id'))
    user_action = Column(types.Enum(User_Action_Audit), nullable=False)
    user_action_desc = Column(types.String(250), nullable=True)
    created_at = Column(types.DateTime, default=datetime.datetime.now)

    doc_class_audit_rel = relationship("Document_Class", back_populates="class_doc_audit_rel")
    doc_user_audit_rel = relationship("User_Info", back_populates="doc_user_audit_rel")