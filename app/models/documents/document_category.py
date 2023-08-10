import datetime
from sqlalchemy import Column, types
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Document_Category(Base):
    __tablename__ = "document_category"
    id = Column(types.Integer, primary_key=True, index=True)
    category = Column(types.String(150), nullable=False)
    category_code = Column(types.Integer, nullable=False)
    created_at = Column(types.DateTime(timezone=True), nullable=False, default=datetime.datetime.now())
    document_usr = relationship("Document_User",
                                primaryjoin="Document_Category.id == Document_User.document_category_code",
                                cascade="all, delete-orphan")

    def __repr__(self):
        return f"Document_Category({self.id}, {self.category}, {self.category_code}, {self.created_at})"

    @property
    def to_json(self):
        return {
            'id': self.id,
            'category': self.category,
            'category_code': self.category_code,
            'created_at': self.created_at
        }
