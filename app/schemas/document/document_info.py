from typing import Optional, List
from pydantic import BaseModel
from app.schemas.schema_utils import to_camel


class DocumentItemInfo_Base(BaseModel):
    class Config:
        alias_generator = to_camel
        populate_by_name = True


class DocumentItemInfo_Show(DocumentItemInfo_Base):
    item_reference: Optional[str] = None
    item_name: Optional[str] = None
    item_cost: Optional[str] = None
    item_tax: Optional[str] = None
    item_tax_rate: Optional[str] = None
    item_rate: Optional[str] = None
    item_quantity: Optional[str] = None

    class Config:
        from_attributes = True


class DocumentHeaderInfo_Base(BaseModel):
    class Config:
        alias_generator = to_camel
        populate_by_name = True


class DocumentHeaderInfo_Show(DocumentHeaderInfo_Base):
    seller_name: Optional[str] = None
    seller_address: Optional[str] = None
    seller_phone: Optional[str] = None
    seller_email: Optional[str] = None
    invoice_date: Optional[str] = None
    invoice_no: Optional[str] = None
    seller_account_no: Optional[str] = None
    buyer_name: Optional[str] = None
    seller_tax_id: Optional[str] = None
    buyer_tax_i: Optional[str] = None

    class Config:
        from_attributes = True


class DocumentSummaryInfo_Base(BaseModel):
    class Config:
        alias_generator = to_camel
        populate_by_name = True


class DocumentSummaryInfo_Show(DocumentSummaryInfo_Base):
    sub_total_return: Optional[str] = None
    sub_total: Optional[str] = None
    total: Optional[str] = None
    gst_included: Optional[str] = None
    tax_amount: Optional[str] = None
    transaction_i: Optional[str] = None

    class Config:
        from_attributes = True


# Schema of User Type Base Class
class DocumentInfo_Base(BaseModel):
    class Config:
        alias_generator = to_camel
        populate_by_name = True


# Schema for Update of Document_User
class DocumentInfo_Show(DocumentInfo_Base):
    document_id: Optional[str] = None
    document_type: Optional[int]
    document_owner: Optional[str] = None
    document_submitted_by: Optional[str] = None
    document_currency: Optional[str] = None
    document_process_time_sec: Optional[float] = None
    doc_header: Optional[DocumentHeaderInfo_Show] = None
    doc_items: Optional[List[DocumentItemInfo_Show]] = None
    doc_summary: Optional[DocumentSummaryInfo_Show] = None

    class Config:
        from_attributes = True

# # Schema for User Type Retrieval
# class DocumentUser(DocumentInfo_Base):
#     id: int
#     user_id: int
#     document_id: str
#     document_filename: str
#     document_source: DocumentSrc
#     document_type: DocumentType
#     document_class: int
#     document_location: Optional[str] = None
#     document_password: Optional[str] = None
#     document_category_code: int
#     document_pages: Optional[int]
#     document_state: DocumentState
#     document_confidence: Optional[float]
#     document_review: DocumentReview
#     document_is_deleted: bool
#     document_process_time_sec: Optional[float]
#     created_at: datetime
#     updated_at: Optional[datetime] = None
#
#     class Config:
#         from_attributes = True
