import datetime
import enum
from werkzeug.security import generate_password_hash
from sqlalchemy import Column, types, ForeignKey, PrimaryKeyConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base_class import Base


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
    id = Column(types.Integer, primary_key=True, index=True)
    user_id = Column(types.Integer, ForeignKey('user_info.id'), nullable=False)
    document_id = Column(types.String(150), nullable=False, unique=True)
    document_source = Column(types.Enum(DocumentSrc), nullable=False)
    document_type = Column(types.Enum(DocumentType), nullable=False)
    document_class = Column(types.Integer, ForeignKey('document_class.id'), nullable=False)
    document_location = Column(types.String(200), nullable=True)
    document_password = Column(types.String(200), nullable=True)
    document_category_code = Column(types.Integer, ForeignKey('document_category.id'), nullable=False)
    document_pages = Column(types.Integer, nullable=True)
    document_state = Column(types.Enum(DocumentState), nullable=False)
    document_confidence = Column(types.Float, nullable=True)
    document_review = Column(types.Enum(DocumentReview), nullable=True)
    document_is_deleted = Column(types.Boolean, nullable=False)
    document_process_time_sec = Column(types.Float, nullable=True)
    created_at = Column(types.DateTime(timezone=True), nullable=False, default=datetime.datetime.now())
    updated_at = Column(types.DateTime(timezone=True), nullable=True,
                        onupdate=datetime.datetime.now())

    document_audit = relationship("Document_Audit_Trail",
                                  primaryjoin="Document_User.document_id == Document_Audit_Trail.document_id",
                                  cascade="all, delete-orphan")

    def set_document_id(self, filename):
        """Create hashed password."""
        self.document_id = generate_password_hash(
            filename,
            method='md5'
        )
