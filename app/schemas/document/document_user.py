from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.schemas.schema_utils import to_camel
from app.models.documents.document_user import DocumentSrc, DocumentType, DocumentReview, DocumentState


# Schema of User Type Base Class
class DocumentUser_Base(BaseModel):
    document_id: Optional[str] = None

    class Config:
        alias_generator = to_camel
        populate_by_name = True


# Schema for Update of Document_User
class DocumentUser_Update(DocumentUser_Base):
    document_id: str
    document_source: Optional[DocumentSrc]
    document_type: Optional[DocumentType]
    document_class: Optional[int]
    document_location: Optional[str]
    document_password: Optional[str]
    document_category_code: Optional[int]
    document_pages: Optional[int] = 0
    document_state: Optional[DocumentState]
    document_confidence: Optional[float]
    document_review: Optional[DocumentReview]
    document_is_deleted: Optional[bool]
    document_process_time_sec: Optional[float]


# Schema for User Type Creation
class DocumentUser_Create(DocumentUser_Base):
    user_id: int
    document_id: str
    document_filename: Optional[str] = None
    document_source: DocumentSrc = DocumentSrc.upload
    document_type: DocumentType = DocumentType.not_scanned
    document_class: int = 1
    document_location: Optional[str] = None
    document_password: Optional[str] = None
    document_category_code: int = 1
    document_state: DocumentState = DocumentState.created
    document_review: DocumentReview = DocumentReview.not_required
    document_is_deleted: bool = False

    class Config:
        from_attributes = True
        alias_generator = to_camel
        populate_by_name = True


class DocumentUser_Upload(DocumentUser_Base):
    document_source: DocumentSrc = DocumentSrc.upload
    document_type: DocumentType = DocumentType.not_scanned
    document_class: int = 1
    document_location: Optional[str] = None
    document_password: Optional[str] = None
    document_category_code: int = 1
    document_state: DocumentState = DocumentState.created
    document_review: DocumentReview = DocumentReview.not_required
    document_is_deleted: bool = False

    class Config:
        from_attributes = True
        alias_generator = to_camel
        populate_by_name = True


class DocumentUser_Delete(DocumentUser_Base):
    user_id: int
    document_id: str
    document_is_delete: bool

    class Config:
        from_attributes = True
        alias_generator = to_camel
        populate_by_name = True


# Schema for User Type Retrieval
class DocumentUser(DocumentUser_Base):
    id: int
    user_id: int
    document_id: str
    document_filename: str
    document_source: DocumentSrc
    document_type: DocumentType
    document_class: int
    document_location: Optional[str] = None
    document_password: Optional[str] = None
    document_category_code: int
    document_pages: Optional[int]
    document_state: DocumentState
    document_confidence: Optional[float]
    document_review: DocumentReview
    document_is_deleted: bool
    document_process_time_sec: Optional[float]
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
