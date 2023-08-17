import sqlalchemy
from typing import Optional

from sqlalchemy.orm import Session
from app.models.documents.document_class import Document_Class,Doc_Class
from app.schemas.document.document_class import DocumentClass_Create, DocumentClass_Update
from app.crud.base import BaseService
from sqlalchemy.exc import IntegrityError
from starlette.exceptions import HTTPException


class DocumentClassService(BaseService[Document_Class, DocumentClass_Create, DocumentClass_Update]):

    def get_by_docclassId(self, db_session: Session, doc_class_id: int) -> Optional[Document_Class]:
        return db_session.query(Document_Class).filter(Document_Class.id == doc_class_id).one_or_none()

    def get_by_docclass(self, db_session: Session, doc_class: Doc_Class) -> Optional[Document_Class]:
        return db_session.query(Document_Class).filter(Document_Class.doc_class == doc_class).first()

    def get_by_docclassCode(self, db_session: Session, doc_class_code: int) -> Optional[Document_Class]:
        return db_session.query(Document_Class).filter(Document_Class.doc_class_code == doc_class_code).first()

    def create(self, db_session: Session, obj_in: DocumentClass_Create) -> Document_Class:
        db_obj = Document_Class(
            doc_class=obj_in.doc_class,
            doc_class_code=obj_in.doc_class_code
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


get_document_class_service = DocumentClassService(Document_Class)
