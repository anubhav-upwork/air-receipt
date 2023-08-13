import sqlalchemy
from typing import Optional

from sqlalchemy.orm import Session
from app.models.documents.document_category import Document_Category
from app.schemas.document.document_category import DocumentCategory_Create, DocumentCategory_Update, DocumentCategory
from app.crud.base import BaseService
from sqlalchemy.exc import IntegrityError
from starlette.exceptions import HTTPException


class DocumentCategoryService(BaseService[Document_Category, DocumentCategory_Create, DocumentCategory_Update]):

    def get_by_doccategory(self, db_session: Session, doc_cat: str) -> Optional[Document_Category]:
        return db_session.query(Document_Category).filter(Document_Category.category == str).first()

    def get_by_doccatcode(self, db_session: Session, code: int) -> Optional[Document_Category]:
        return db_session.query(Document_Category).filter(Document_Category.category_code == code).first()

    def create(self, db_session: Session, obj_in: DocumentCategory_Create) -> Document_Category:
        db_obj = Document_Category(
            category=obj_in.category,
            category_code=obj_in.category_code
        )
        db_session.add(db_obj)
        try:
            db_session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            db_session.rollback()
            if "duplicate key" in str(e):
                raise HTTPException(status_code=409, detail="Conflict Error")
            else:
                raise e
        db_session.refresh(db_obj)
        return db_obj


get_document_category_service = DocumentCategoryService(Document_Category)
