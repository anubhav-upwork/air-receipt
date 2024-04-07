import sqlalchemy
from typing import Optional, List

from sqlalchemy.orm import Session
from app.models.documents.document_user import DocumentSrc, DocumentType, DocumentReview, DocumentState, Document_User
from app.schemas.document.document_user import DocumentUser_Update, DocumentUser_Create, DocumentUser
from app.models.documents.document_class import Document_Class, Doc_Class
from app.crud.base import BaseService
from sqlalchemy.exc import IntegrityError
from starlette.exceptions import HTTPException


class DocumentUserService(BaseService[Document_User, DocumentUser_Create, DocumentUser_Update]):

    def get_by_doc_id(self, db_session: Session, doc_id: str) -> Optional[Document_User]:
        return db_session.query(Document_User).filter(Document_User.document_id == doc_id).first()

    def list_by_user_id(self, db_session: Session, user_id: int) -> Optional[List[Document_User]]:
        return db_session.query(Document_User).filter(Document_User.user_id == user_id).all()

    def list_by_user_id_done(self, db_session: Session, user_id: int) -> Optional[List[Document_User]]:
        return (db_session.query(Document_User).filter(Document_User.user_id == user_id)
                .filter(Document_User.document_state == DocumentState.processed).all())

    def list_by_type(self, db_session: Session, doc_type: DocumentType) -> Optional[List[Document_User]]:
        return db_session.query(Document_User).filter(Document_User.document_type == doc_type).all()

    def list_by_source(self, db_session: Session, doc_src: DocumentSrc) -> Optional[List[Document_User]]:
        return db_session.query(Document_User).filter(Document_User.document_source == doc_src).all()

    def list_by_user_id_paginated(self, db_session: Session, user_id: int, skip: int = 0, limit: int = 10) -> Optional[
        List[Document_User]]:
        return (db_session.query(Document_User).filter(Document_User.user_id == user_id)
                .offset((skip-1)*limit).limit(limit).all())

    def get_user_document_count(self, db_session: Session, user_id: int) -> int:
        no_docs = db_session.query(Document_User).filter(Document_User.user_id == user_id).count()
        return no_docs

    def create(self, db_session: Session, obj_in: DocumentUser_Create) -> Document_User:
        db_obj = Document_User(
            user_id=obj_in.user_id,
            document_id=obj_in.document_id,  # this should be unique always
            document_filename=obj_in.document_filename,
            document_source=obj_in.document_source,
            document_type=obj_in.document_type,
            document_class=obj_in.document_class,
            document_location=obj_in.document_location,
            document_password=obj_in.document_password,
            document_category_code=obj_in.document_category_code,
            document_pages=obj_in.document_pages,
            document_state=obj_in.document_state,
            document_review=obj_in.document_review,
            document_is_deleted=False
        )

        # Check for Foreign Associations and validate
        doc_class_exists = db_session.query(Document_Class).filter(Document_Class.id == obj_in.document_class).first()

        if not doc_class_exists:
            raise HTTPException(status_code=400, detail=f"Document Class Type does not exist {obj_in.document_class} ")

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
