from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.documents.document_class import Document_Class, Doc_Class
from app.schemas.document.document_class import DocumentClass, DocumentClass_Create, DocumentClass_Update
from app.crud.document.document_class import get_document_class_service
from app.api import deps

router = APIRouter(prefix="/doc-class", tags=["Document Class"])


@router.post("/create_doc_class", status_code=201, response_model=DocumentClass)
async def create_doc_class(dc: DocumentClass_Create,
                           db: Session = Depends(deps.get_db)) -> Document_Class:
    existing_class = get_document_class_service.get_by_docclass(db_session=db, doc_class=dc.doc_class)
    existing_class_code = get_document_class_service.get_by_docclassCode(db_session=db,
                                                                         doc_class_code=dc.doc_class_code)
    if existing_class or existing_class_code:
        raise HTTPException(
            status_code=400, detail="Document Class or Code already exists"
        )
    return get_document_class_service.create(db_session=db, obj_in=dc)


@router.get("/", status_code=201, response_model=List[DocumentClass])
async def list_doc_class(db: Session = Depends(deps.get_db)) -> List[Document_Class]:
    return get_document_class_service.list(db_session=db)
