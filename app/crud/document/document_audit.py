from typing import Optional, List, Any

import sqlalchemy
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette.exceptions import HTTPException

from app.crud.base import BaseService
from app.models.documents.document_action_audit import Document_Audit_Trail
from app.schemas.document.document_audit_trail import DocumentAudit_Create, DocumentAudit_Update


class DocumentAuditService(BaseService[Document_Audit_Trail, DocumentAudit_Create, DocumentAudit_Update]):

    def list_by_docId(self, db_session: Session, docId: str) -> Optional[List[Document_Audit_Trail]]:
        return db_session.query(Document_Audit_Trail).filter(Document_Audit_Trail.document_id == docId).all()

    def create(self, db_session: Session, obj_in: DocumentAudit_Create) -> Document_Audit_Trail:
        db_obj = Document_Audit_Trail(
            document_id=obj_in.document_id,
            action=obj_in.action,
            action_msg=obj_in.action_msg
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

    def update(self, db_session: Session, _id: Any, obj: DocumentAudit_Update) -> Optional[Document_Audit_Trail]:
        raise HTTPException(status_code=501, detail="Updating the Document Audit is not supported")


get_document_audit_service = DocumentAuditService(Document_Audit_Trail)
