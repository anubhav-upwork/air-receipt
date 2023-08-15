from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.schemas.schema_utils import to_camel
from app.models.documents.document_user import DocumentSrc, DocumentType, DocumentReview, DocumentState
from app.models.documents.document_class import Doc_Class

# Schema of User Type Base Class
class DocumentUser_Base(BaseModel):
    user_id: Optional[int]
    document_id: Optional[str]
    document_source: Optional[DocumentSrc]
    document_type: Optional[DocumentType]
    document_class: Optional[Doc_Class]
    document_location: Optional[str]
    document_password: Optional[str]
    document_category_code: Optional[int]
    document_pages: Optional[int]
    document_state: Optional[DocumentState]
    document_confidence: Optional[float]
    document_review: Optional[DocumentReview]
    document_is_deleted: Optional[bool]
    document_process_time_sec: Optional[float]

    class Config:
        alias_generator = to_camel
        populate_by_name = True


# Schema for Update of Document_User
class DocumentUser_Update(DocumentUser_Base):
    ...


# Schema for User Type Creation
class DocumentUser_Create(DocumentUser_Base):
    user_id: int
    document_id: str
    document_source: DocumentSrc
    document_type: DocumentType
    document_class: Doc_Class
    document_location: Optional[str]
    document_password: Optional[str]
    document_category_code: int
    document_state: DocumentState


    class Config:
        from_attributes = True
        alias_generator = to_camel
        populate_by_name = True


# Schema for User Type Retrieval
class DocumentUser(DocumentUser_Base):
    id: int
    user_id: int
    document_id: str
    document_source: DocumentSrc
    document_type: DocumentType
    document_class: Doc_Class
    document_category_code: int
    document_state: DocumentState
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
