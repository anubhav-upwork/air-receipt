from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.schemas.schema_utils import to_camel
from app.models.documents.document_user import DocumentState


# Schema of Document Audit Trail Base
class DocumentAudit_Base(BaseModel):
    class Config:
        alias_generator = to_camel
        populate_by_name = True


class DocumentAudit_Update:
    ...


# Schema for Document Audit Entry
class DocumentAudit_Create(DocumentAudit_Base):
    document_id: str
    action: DocumentState
    action_msg: str

    class Config:
        from_attributes = True


# Schema for Document Audit Retrieval
class DocumentAudit(DocumentAudit_Base):
    id: int
    document_id: str
    action: DocumentState
    action_msg: str
    created_at: datetime

    class Config:
        from_attributes = True
