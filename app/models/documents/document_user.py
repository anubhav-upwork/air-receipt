import datetime
import enum
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, types, ForeignKey, PrimaryKeyConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.dbconnect import Base


class DocumentSrc(str, enum.Enum):
    upload = "UPLOAD"
    api = "API"
    email = "EMAIL"

class DocumentType(str, enum.Enum):
    scan = "SCANNED"
    not_scanned = "NOT_SCANNED"

class DocumentState(str, enum.Enum):
    created = "CREATED"
    queued = "QUEUED"
    inprocess = "IN_PROCESS"
    processed = "PROCESSED"
    failed = "FAILED"

class DocumentReview(str, enum.Enum):
    required = "REQUIRED"
    not_required = "NOT_REQUIRED"
    completed = "COMPLETED"

class Document_User(Base):
    __tablename__ = "document_user"
    id = Column(types.Integer, primary_key=True)
    user_id = Column(types.Integer, ForeignKey('users_info.id'))
    document_id = Column(types.Text, nullable=False)
    document_source = Column(types.Enum(DocumentSrc), nullable=False)
    document_type = Column(types.Enum(DocumentType), nullable=False)
    document_class = Column(types.Integer,ForeignKey('document_class.id'))
    document_location = Column(types.Text, nullable=False)
    document_category_code = Column(types.Integer, ForeignKey('document_category.id'))
    document_pages = Column(types.Integer, nullable=True)
    document_state = Column(types.Enum(DocumentState), nullable=False)
    document_confidence = Column(types.Float, nullable=False)
    document_review = Column(types.Enum(DocumentReview), nullable=False)
    document_is_deleted = Column(types.Boolean, nullable=False)
    document_process_time_sec = Column(types.Float, nullable=False)
    created_at = Column(types.DateTime, default=datetime.datetime.now)
    updated_at = Column(types.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    doc_class_rel = relationship("Document_Class", back_populates="u_info")
    u_role = relationship("User_Roles", back_populates="u_info")

    __table_args__ = (
        PrimaryKeyConstraint('id', name='user_pk'),
        UniqueConstraint('document_id'),
    )

    def set_document_id(self, filename):
        """Create hashed password."""
        self.document_id = generate_password_hash(
            filename,
            method='md5'
        )