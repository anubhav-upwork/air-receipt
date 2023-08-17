import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash

from app.api import deps
from app.models.user.user_info import User_Info
from app.models.documents.document_user import Document_User, DocumentSrc, DocumentType, DocumentState, DocumentReview
from app.schemas.document.document_user import DocumentUser, DocumentUser_Create, DocumentUser_Update, \
    DocumentUser_Upload
from app.crud.document.document_user import get_document_user_service
from app.crud.document.document_category import get_document_category_service
from app.crud.document.document_class import get_document_class_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/documents", tags=["Document"])


@router.post("/upload_document", status_code=201, response_model=DocumentUser)
async def upload_document(du: DocumentUser_Upload = Depends(),
                          file: UploadFile = File(...),
                          db: Session = Depends(deps.get_db),
                          cur_user: User_Info = Depends(deps.get_current_user)) -> Document_User:
    logger.info(f"Document Received: from:{cur_user.id}, file:{file.filename},"
                f" State:{du.document_state},"
                f" ClassId:{du.document_class}")

    file_name_hash = generate_password_hash(file.filename, method='md5')
    existing_filehash = get_document_user_service.get_by_doc_id(db_session=db, doc_id=file_name_hash)
    existing_class_code = get_document_class_service.get_by_docclassId(db_session=db,
                                                                       doc_class_id=du.document_class)
    existing_category_code = get_document_category_service.get_by_doccatcode(db_session=db,
                                                                             code=du.document_category_code)

    if not existing_class_code:
        raise HTTPException(
            status_code=400, detail="Document Class does not exist!"
        )

    if not existing_category_code:
        raise HTTPException(
            status_code=400, detail=f"Document Category {du.document_category_code} does not exist !"
        )

    if existing_filehash:
        raise HTTPException(
            status_code=400, detail="Document with same hash exists"
        )

    dc = DocumentUser_Create(
        user_id=cur_user.id,
        document_id=file_name_hash,
        document_filename=file.filename,
        document_source=du.document_source,
        document_type=du.document_type,
        document_class=du.document_class,
        document_location=du.document_location,
        document_password=du.document_password,
        document_category_code=existing_category_code.id,
        document_state=du.document_state,
        document_review=du.document_review,
        document_is_deleted=du.document_is_deleted
    )
    # assign data from file
    return get_document_user_service.create(db_session=db, obj_in=dc)


@router.get("/document", status_code=201, response_model=List[DocumentUser])
async def list_user_documents(db: Session = Depends(deps.get_db),
                              cur_user: User_Info = Depends(deps.get_current_user)
                              ) -> List[Document_User]:
    return get_document_user_service.list_by_user_id(db_session=db, user_id=cur_user.id)
