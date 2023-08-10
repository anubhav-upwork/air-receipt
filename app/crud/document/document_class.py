import sqlalchemy
from typing import Optional

from sqlalchemy.orm import Session
from app.models.documents.document_class import Document_Class
from app.schemas.document.document_class import DocumentClass_Create, DocumentClass_Update
from app.crud.base import BaseService
from sqlalchemy.exc import IntegrityError
from starlette.exceptions import HTTPException


class DocumentClassService(BaseService[Document_Class, DocumentClass_Create, DocumentClass_Update]):

    def get_by_docclass(self, db_session: Session, role: str) -> Optional[Document_Class]:
        return db_session.query(Document_Class).filter(Document_Class.doc_class == role).first()

    # def create(self, db_session: Session, obj_in: DocumentClass_Create) -> Document_Class:
    #     db_obj = User_Roles(
    #         user_role=obj_in.user_role,
    #         user_access_level=obj_in.user_access_level
    #     )
    #     self.db_session.add(db_obj)
    #     try:
    #         self.db_session.commit()
    #     except sqlalchemy.exc.IntegrityError as e:
    #         self.db_session.rollback()
    #         if "duplicate key" in str(e):
    #             raise HTTPException(status_code=409, detail="Conflict Error")
    #         else:
    #             raise e
    #     self.db_session.refresh(db_obj)
    #     return db_obj
