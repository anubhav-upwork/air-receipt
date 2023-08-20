import os
from typing import List
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Form
from sqlalchemy.orm import Session
from app.core.airlogger import logger
from app.api import deps
from app.core import utils
from app.core.config import settings
from app.models.user.user_info import User_Info
from app.models.documents.document_user import Document_User, DocumentSrc, DocumentType, DocumentState, DocumentReview
from app.schemas.document.document_user import DocumentUser, DocumentUser_Create, DocumentUser_Update, \
    DocumentUser_Upload
from app.crud.document.document_user import get_document_user_service
from app.crud.document.document_category import get_document_category_service
from app.crud.document.document_class import get_document_class_service

router = APIRouter(prefix="/documents", tags=["Document"])


@router.post("/upload_document", status_code=201, response_model=DocumentUser)
async def upload_document(du: DocumentUser_Upload = Depends(),
                          file: UploadFile = File(...),
                          db: Session = Depends(deps.get_db),
                          cur_user: User_Info = Depends(deps.get_current_user)) -> Document_User:
    _file_save_path = str(settings.UPLOAD_PATH) + "/" + str(cur_user.id)
    logger.info(f"Document Received: from:{cur_user.id}, file:{file.filename},"
                f" State:{du.document_state},"
                f" ClassId:{du.document_class}")

    # Check if file store path exists, if not create dir
    if not os.path.isdir(_file_save_path):
        os.makedirs(_file_save_path)

    _filename = file.filename
    _file_content_type = file.content_type
    _filename_len = len(file.filename.split('.'))

    _extension = file.filename.split('.')[_filename_len - 1].lower()  # Save the extension of the file for upload
    logger.info(f"File extension : <{_extension}>, filename <{_filename}>,"
                f" uploaded by <{cur_user.user_name}>,"
                f" content-type <{_file_content_type}>")

    if _file_content_type not in settings.ALLOWED_CONTENT:
        raise HTTPException(
            status_code=400, detail="Content Type Not Allowed!"
        )

    file_name_hash = utils.generate_file_name(8) + f".{_extension}"

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

    try:
        content = await file.read()
        with open(_file_save_path + "/" + file_name_hash, 'wb') as f:
            f.write(content)
    except Exception as ex:
        raise HTTPException(
            status_code=400, detail="File writing error"
        )

    dc = DocumentUser_Create(
        user_id=cur_user.id,
        document_id=file_name_hash,
        document_filename=_filename,
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


@router.patch("/update", status_code=201, response_model=DocumentUser)
async def update_document(du: DocumentUser_Update,
                          db: Session = Depends(deps.get_db),
                          cur_user: User_Info = Depends(deps.get_current_user)
                          ) -> Document_User:

    existing_filehash = get_document_user_service.get_by_doc_id(db_session=db, doc_id=du.document_id)
    if not existing_filehash:
        raise HTTPException(
            status_code=400, detail=f"Document with filename {du.document_id} does not exist!"
        )

    return get_document_user_service.update(db_session=db, _id=existing_filehash.id, obj=du)


# @router.patch("/delete", status_code=201, response_model=DocumentUser)
# async def delete_document(du: DocumentUser_Update,
#                           db: Session = Depends(deps.get_db),
#                           cur_user: User_Info = Depends(deps.get_current_user)
#                           ) -> Document_User:
#
#
#     return get_document_user_service.list_by_user_id(db_session=db, user_id=cur_user.id)
