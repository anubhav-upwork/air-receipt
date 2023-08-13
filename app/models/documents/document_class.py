import datetime
import enum
from sqlalchemy import Column, types
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Doc_Class(str, enum.Enum):
    invoice = "INVOICE"
    receipt = "RECEIPT"
    credit_note = "CREDIT_NOTE"
    other = "OTHER"


class Document_Class(Base):
    __tablename__ = "document_class"
    id = Column(types.Integer, primary_key=True, index=True)
    doc_class = Column(types.Enum(Doc_Class), nullable=False)
    doc_class_code = Column(types.Integer, nullable=False, unique=True)
    created_at = Column(types.DateTime(timezone=True), nullable=False, default=datetime.datetime.now())

    # document_usr = relationship("Document_User", primaryjoin="Document_Class.id == Document_User.document_class",
    #                             cascade="all, delete-orphan")

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
