from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.documents.document_category import Document_Category
from app.schemas.document.document_category import DocumentCategory, DocumentCategory_Create, DocumentCategory_Update
from app.crud.document.document_category import get_document_category_service
from app.api import deps

router = APIRouter(prefix="/doc-category", tags=["Document"])


@router.post("/create_doc_category", status_code=201, response_model=DocumentCategory)
async def create_doc_category(dc: DocumentCategory_Create,
                              db: Session = Depends(deps.get_db)) -> Document_Category:
    existing_category = get_document_category_service.get_by_doccategory(db_session=db,
                                                                         doc_cat=dc.category)
    existing_cat_code = get_document_category_service.get_by_doccatcode(db_session=db,
                                                                        code=dc.category_code)
    if existing_category or existing_cat_code:
        raise HTTPException(
            status_code=400, detail="Document Category or Code already exists"
        )
    return get_document_category_service.create(db_session=db, obj_in=dc)


@router.get("/", status_code=201, response_model=List[DocumentCategory])
async def list_doc_category(db: Session = Depends(deps.get_db)) -> List[Document_Category]:
    return get_document_category_service.list(db_session=db)
