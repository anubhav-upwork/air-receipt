import datetime
import enum
from sqlalchemy import Column, types
from sqlalchemy.orm import relationship
from app.db.dbconnect import Base


class DocumentClass(str, enum.Enum):
    invoice = "INVOICE"
    receipt = "RECEIPT"
    other   = "OTHER"

class Document_Class(Base):
    __tablename__ = "document_class"
    id = Column(types.Integer, primary_key=True)
    doc_class = Column(types.String(150), nullable=False)
    doc_class_code = Column(types.Integer, nullable=False)
    created_at = Column(types.DateTime, default=datetime.datetime.now)
    class_doc_rel = relationship('Document_User', backref = "doc_class_rel")
    
    def __repr__(self):
        return f"Document_Class({self.id}, {self.doc_class}, {self.doc_class_code}, {self.created_at})"
        
    @property
    def to_json(self):
        return {
            'id': self.id,
            'doc_class': self.doc_class,
            'doc_class_code': self.doc_class_code,
            'created_at': self.created_at
        }
    
