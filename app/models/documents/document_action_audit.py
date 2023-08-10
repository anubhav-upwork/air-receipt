import datetime
from sqlalchemy import Column, types, ForeignKey
from app.db.base_class import Base
from app.models.documents.document_user import DocumentState


class Document_Audit_Trail(Base):
    __tablename__ = "document_audit_trail"
    id = Column(types.Integer, primary_key=True)
    document_id = Column(types.String(150), ForeignKey('document_user.document_id'), nullable=False)
    action = Column(types.Enum(DocumentState), nullable=False)
    action_msg = Column(types.String(250), nullable=True)
    created_at = Column(types.DateTime, nullable=False, default=datetime.datetime.now())
