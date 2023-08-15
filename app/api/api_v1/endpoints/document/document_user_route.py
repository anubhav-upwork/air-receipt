from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.user.user_info import User_Info
from app.models.documents.document_user import Document_User, DocumentSrc, DocumentType, DocumentState, DocumentReview
from app.schemas.document.document_user import DocumentUser, DocumentUser_Create, DocumentUser_Update
from app.crud.document.document_user import get_document_user_service
from app.crud.document.document_category import get_document_category_service
from app.crud.user.user_info import get_user_info_service
from werkzeug.security import generate_password_hash
from app.api import deps

router = APIRouter(prefix="/documents", tags=["Document"])


@router.post("/create_document", status_code=201, response_model=DocumentUser)
async def create_document(dc: DocumentUser_Create,
                          db: Session = Depends(deps.get_db),
                          cur_user: User_Info = Depends(deps.get_current_user)) -> Document_User:
    file_name_hash = generate_password_hash(dc.document_id, method='md5')
    existing_filehash = get_document_user_service.get_by_doc_id(db_session=db, doc_id=file_name_hash)
    # existing_class_code = get_document_class_service.get_by_docclasscode(db_session=db,
    #                                                                      doc_class_code=dc.doc_class_code)
    if existing_filehash:
        raise HTTPException(
            status_code=400, detail="Document Class or Code already exists"
        )

    dc.document_id = file_name_hash
    return get_document_user_service.create(db_session=db, obj_in=dc)


@router.get("/document", status_code=201, response_model=List[DocumentUser])
async def list_doc_class(db: Session = Depends(deps.get_db),
                         cur_user: User_Info = Depends(deps.get_current_user)
                         ) -> List[Document_User]:
    return get_document_user_service.list_by_user_id(db_session=db, user_id=cur_user.id)
