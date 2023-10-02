from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.schemas.schema_utils import to_camel


class Kafka_Document(BaseModel):
    user_id: int
    document_id: str
    document_filename: str
    document_password: Optional[str] = None
    document_pages: int
    document_size: float = 0.0
    document_extension: str
    document_push_time: str = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    class Config:
        from_attributes = True
        alias_generator = to_camel
        populate_by_name = True
