import enum
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.schemas.schema_utils import to_camel


# Schema of User Type Base Class
class DocumentClass_Base(BaseModel):
    doc_class: enum.Enum
    doc_class_code: int

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


# Schema for Update of User_Type
class DocumentClass_Update(DocumentClass_Base):
    doc_class: Optional[enum.Enum]
    doc_class_code: Optional[int]


# Schema for User Type Creation
class DocumentClass_Create(DocumentClass_Base):
    pass


# Schema for User Type Retrieval
class DocumentClass(DocumentClass_Base):
    id: int
    doc_class: enum.Enum
    doc_class_code: int
    created_at: datetime

    class Config:
        orm_mode = True
