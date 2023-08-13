import enum
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.schemas.schema_utils import to_camel
from app.models.documents.document_class import Doc_Class


# Schema of DocumentClass Base Class
class DocumentClass_Base(BaseModel):
    doc_class: Doc_Class
    doc_class_code: int

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


# Schema for Update of User_Type
class DocumentClass_Update(DocumentClass_Base):
    doc_class: Optional[Doc_Class]
    doc_class_code: Optional[int]


# Schema for User Type Creation
class DocumentClass_Create(DocumentClass_Base):
    pass


# Schema for User Type Retrieval
class DocumentClass(BaseModel):
    id: int
    doc_class: str
    doc_class_code: int
    created_at: datetime

    class Config:
        from_attributes = True
