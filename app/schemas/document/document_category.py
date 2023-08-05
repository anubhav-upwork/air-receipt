from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.schemas.schema_utils import to_camel


# Schema of User Type Base Class
class DocumentCategory_Base(BaseModel):
    category: str
    category_code: int

    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True


# Schema for Update of User_Type
class DocumentCategory_Update(DocumentCategory_Base):
    category: Optional[str]
    category_code: Optional[int]


# Schema for User Type Creation
class DocumentCategory_Create(DocumentCategory_Base):
    pass


# Schema for User Type Retrieval
class DocumentCategory(DocumentCategory_Base):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
