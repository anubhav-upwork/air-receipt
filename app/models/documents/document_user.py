import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, types, ForeignKey, PrimaryKeyConstraint, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.dbconnect import Base


class DocumentSrc(str, types.Enum):
    direct_upload = "Direct_Upload"
    api = "API"
    email = "Email" 

class DocumentType(str, types.Enum):
    scan = "Scanned"
    not_scanned = "Not_Scanned"

class DocumentClass(str, types.Enum):
    invoice = "Invoice"
    receipt = "Receipt"
    other   = "Other"

class DocumentState(str, types.Enum):
    created = "Created"
    queued = "Queued"
    inprocess = "In_Process"
    processed = "Processed"
    failed = "Failed"

class DocumentReview(str, types.Enum):
    required = "Required"
    not_required = "Not_Required"
    completed = "Completed"

class Document_User(Base):
    __tablename__ = "document_user"
    id = Column(types.Integer, primary_key=True)
    user_id = Column(types.String(50), nullable=False)
    document_id = Column(types.String(150), nullable=False)
    user_email = Column(types.String(255), unique=True, nullable=False)
    user_mobile = Column(types.String(20), unique=True, nullable=False)
    user_location = Column(types.String(255), nullable=False)
    user_password = Column(types.Text, nullable=False)
    user_role = Column(types.Integer, ForeignKey('user_roles.id'))
    user_type = Column(types.Integer, ForeignKey('user_types.id'))
    user_credit = Column(types.Float, nullable=False)
    user_is_deleted = Column(types.Boolean, nullable=False)
    user_is_active = Column(types.Boolean, nullable=False)
    created_at = Column(types.DateTime, default=datetime.datetime.now)
    updated_at = Column(types.DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now)
    u_type = relationship("User_Types", back_populates="u_info")
    u_role = relationship("User_Roles", back_populates="u_info")

    __table_args__ = (
        PrimaryKeyConstraint('id', name='user_pk'),
        UniqueConstraint('user_name'),
        UniqueConstraint('user_email')
    )

    def set_document_id(self, filename):
        """Create hashed password."""
        self.document_id = generate_password_hash(
            filename,
            method='md5'
        )