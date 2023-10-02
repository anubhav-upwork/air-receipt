from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user.user_info import User_Info

from app.crud.document.document_category import get_document_category_service
from app.models.documents.document_category import Document_Category
from app.schemas.document.document_category import DocumentCategory, DocumentCategory_Create

router = APIRouter(prefix="/doc-category", tags=["Document Category"])


@router.post("/create_doc_category", status_code=status.HTTP_201_CREATED, response_model=DocumentCategory)
async def create_doc_category(dc: DocumentCategory_Create,
                              db: Session = Depends(deps.get_db),
                              cur_user: User_Info = Depends(deps.get_current_user)) -> Document_Category:
    """
        API for creating Document Categories which specify to which sector it belongs to.
    @param dc: Input Document Category Create Pydantic Object
    @param db: Input DB session
    @param cur_user: Input current user session to restrict access
    @return: Output Document Category Pydantic Object
    """
    if not cur_user.user_is_superuser:
        raise HTTPException(
            status_code=401, detail="Not authorized to access this"
        )

    existing_category = get_document_category_service.get_by_doccategory(db_session=db,
                                                                         doc_cat=dc.category)
    existing_cat_code = get_document_category_service.get_by_doccatcode(db_session=db,
                                                                        code=dc.category_code)
    if existing_category or existing_cat_code:
        raise HTTPException(
            status_code=400, detail="Document Category or Code already exists"
        )
    return get_document_category_service.create(db_session=db, obj_in=dc)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[DocumentCategory])
async def list_doc_category(db: Session = Depends(deps.get_db),
                            cur_user: User_Info = Depends(deps.get_current_user)) -> List[Document_Category]:
    """
    API to list Document Categories
    @param db: Input DB session
    @param cur_user: Input current user session to restrict access
    @return: Output list of Document Categories listed as list of pydantic objects
    """
    if not cur_user.user_is_superuser:
        raise HTTPException(
            status_code=401, detail="Not authorized to access this"
        )
    return get_document_category_service.list(db_session=db)
