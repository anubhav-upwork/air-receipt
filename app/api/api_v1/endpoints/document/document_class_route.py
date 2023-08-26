from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user.user_info import User_Info
from app.crud.document.document_class import get_document_class_service
from app.models.documents.document_class import Document_Class
from app.schemas.document.document_class import DocumentClass, DocumentClass_Create

router = APIRouter(prefix="/doc-class", tags=["Document Class"])


@router.post("/create_doc_class", status_code=201, response_model=DocumentClass)
async def create_doc_class(dc: DocumentClass_Create,
                           db: Session = Depends(deps.get_db),
                           cur_user: User_Info = Depends(deps.get_current_user)) -> Document_Class:
    """
        API for creating Document Class. Document Classes can be either of these below:
            INVOICE	1000
            RECEIPT	1001
            CREDIT_NOT	1002
            OTHER	1003
    @param cur_user: Input Current User (Dependency Injection)
    @param dc: Input Document Class Create Pydantic Object
    @param db: Input DB session
    @return: Outputs Document Class Pydantic
    """

    if not cur_user.user_is_superuser:
        raise HTTPException(
            status_code=401, detail="Not authorized to access this"
        )

    existing_class = get_document_class_service.get_by_docclass(db_session=db, doc_class=dc.doc_class)
    existing_class_code = get_document_class_service.get_by_docclassCode(db_session=db,
                                                                         doc_class_code=dc.doc_class_code)
    if existing_class or existing_class_code:
        raise HTTPException(
            status_code=400, detail="Document Class or Code already exists"
        )
    return get_document_class_service.create(db_session=db, obj_in=dc)


@router.get("/", status_code=201, response_model=List[DocumentClass])
async def list_doc_class(db: Session = Depends(deps.get_db),
                         cur_user: User_Info = Depends(deps.get_current_user)) -> List[Document_Class]:
    """
    API for listing all the stored Document Classes
    @param cur_user: Input Current User (Dependency Injection)
    @param db: Input DB session
    @return: Outputs List Document Class Pydantic
    """

    if not cur_user.user_is_superuser:
        raise HTTPException(
            status_code=401, detail="Not authorized to access this"
        )

    return get_document_class_service.list(db_session=db)
