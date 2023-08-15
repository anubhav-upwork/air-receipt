import sqlalchemy
from typing import Optional, List

from sqlalchemy.orm import Session
from app.models.documents.document_user import DocumentSrc, DocumentType, DocumentReview, DocumentState, Document_User
from app.schemas.document.document_user import DocumentUser_Update, DocumentUser_Create, DocumentUser
from app.crud.base import BaseService
from sqlalchemy.exc import IntegrityError
from starlette.exceptions import HTTPException


class DocumentUserService(BaseService[Document_User, DocumentUser_Create, DocumentUser_Update]):

    def get_by_doc_id(self, db_session: Session, doc_id: str) -> Optional[Document_User]:
        return db_session.query(Document_User).filter(Document_User.document_id == doc_id).first()

    def list_by_user_id(self, db_session: Session, user_id: int) -> Optional[List[Document_User]]:
        return db_session.query(Document_User).filter(Document_User.user_id == user_id).all()

    def list_by_type(self, db_session: Session, doc_type: DocumentType) -> Optional[List[Document_User]]:
        return db_session.query(Document_User).filter(Document_User.document_type == doc_type).all()

    def list_by_source(self, db_session: Session, doc_src: DocumentSrc) -> Optional[List[Document_User]]:
        return db_session.query(Document_User).filter(Document_User.document_source == doc_src).all()

    def create(self, db_session: Session, obj_in: DocumentUser_Create) -> Document_User:
        db_obj = Document_User(
            user_id=obj_in.user_id,
            document_id=obj_in.document_id,  # this should be unique always
            document_source=obj_in.document_source,
            document_type=obj_in.document_type,
            document_class=obj_in.document_class,
            document_location=obj_in.document_location,
            document_password=obj_in.document_password,
            document_category_code=obj_in.document_category_code,
            document_pages=obj_in.document_pages,
            document_state=obj_in.document_state,
            document_confidence=obj_in.document_confidence,
            document_review=obj_in.document_review,
            document_is_deleted=obj_in.document_is_deleted,
            document_process_time_sec=obj_in.document_process_time_sec
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


get_document_user_service = DocumentUserService(Document_User)
