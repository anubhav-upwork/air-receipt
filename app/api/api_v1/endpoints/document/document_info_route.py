import os
import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.core import utils
from app.core.airlogger import logger
from app.core.config import settings
from app.crud.document.document_audit import get_document_audit_service
from app.crud.document.document_category import get_document_category_service
from app.crud.document.document_class import get_document_class_service
from app.crud.document.document_user import get_document_user_service
from app.crud.user.user_info import get_user_info_service
from app.models.documents.document_user import Document_User, DocumentState
from app.models.user.user_info import User_Info
from app.schemas.document.document_audit_trail import DocumentAudit_Create
from app.schemas.document.document_user import DocumentQuery_Input
from app.schemas.document.document_info import (DocumentItemInfo_Show, DocumentSummaryInfo_Show,
                                                DocumentHeaderInfo_Show, DocumentInfo_Show, DocumentInfoNoLine_Show)
from app.core.http_exceptions import (DuplicateValueException, UnauthorizedException, NotFoundException,
                                      BadRequestException, UnprocessableEntityException,
                                      InternalServerException, InProcessException)

router = APIRouter(prefix="/doc-detail", tags=["Document Details"])


@router.post("/data", status_code=status.HTTP_200_OK, response_model=DocumentInfo_Show)
async def show_document(du: DocumentQuery_Input = Depends(),
                        db: Session = Depends(deps.get_db),
                        cur_user: User_Info = Depends(deps.get_current_user)) -> DocumentInfo_Show:
    # Find & match Document from Document User Table
    existing_doc = get_document_user_service.get_by_doc_id(db_session=db, doc_id=du.document_id)

    if not existing_doc:
        raise NotFoundException(f"Document {du.document_id} Not Found")

    # TODO
    # if not cur_user.user_is_superuser and existing_doc.user_id != du.user_id:
    #     raise UnauthorizedException("You are not authorized to see the document")

    if existing_doc.document_state != DocumentState.processed:
        raise InProcessException("Document is still in processing")

    _file_save_path = f"{settings.UPLOAD_PATH}/{existing_doc.user_id}/{existing_doc.document_id.split('.', 1)[0]}/pg1_raw.json"
    logger.info(f"Document Show Request Received: from:{cur_user.id} save path {_file_save_path}")

    # Check if a file store path exists, if not create dir
    if not os.path.isfile(_file_save_path):
        raise NotFoundException(f"Conversion Details not found for document {du.document_id}")

    doc_owner = get_user_info_service.get_by_uid(db_session=db, uid=existing_doc.user_id)
    print(doc_owner)
    try:

        # load json file
        with open(_file_save_path, "r") as f:
            raw_json_data = json.load(f)

        # "seller_name": "",
        # "seller_address": "",
        # "seller_phone": "",
        # "seller_email": "",
        # "invoice_date": "",
        # "invoice_no": "",
        # "seller_account_no": "",
        # "buyer_name": "",
        # "seller_tax_id": "",
        # "buyer_tax_id": "",
        # "sub_total_return": "",
        # "sub_total": "",
        # "total": "",
        # "gst_included": "",
        # "tax_amount": "",
        # "transaction_id": ""

        data_schema = DocumentInfoNoLine_Show(**raw_json_data)

        header = DocumentHeaderInfo_Show(
            seller_name=data_schema.seller_name,
            seller_address=data_schema.seller_address,
            seller_phone=data_schema.seller_phone,
            seller_email=data_schema.seller_email,
            invoice_date=data_schema.invoice_date,
            invoice_no=data_schema.invoice_no,
            seller_account_no=data_schema.seller_account_no,
            buyer_name=data_schema.buyer_name,
            seller_tax_id=data_schema.seller_tax_id,
            buyer_tax_id=data_schema.buyer_tax_id
        )

        summary = DocumentSummaryInfo_Show(
            sub_total_return=data_schema.sub_total_return,
            sub_total=data_schema.sub_total,
            total=data_schema.total,
            gst_included=data_schema.gst_included,
            tax_amount=data_schema.tax_amount,
            transaction_i=data_schema.transaction_id
        )
        result: DocumentInfo_Show = DocumentInfo_Show(
            document_id=du.document_id,
            document_type=existing_doc.document_type,
            document_owner=doc_owner.user_name,
            document_submitted_by=doc_owner.user_email,
            document_currency="AUD",
            doc_header=header,
            # doc_items: Optional[List[DocumentItemInf
            doc_summary=summary
        )

        # Audit the document
        # enter into user audit trail
        # audit_log = DocumentAudit_Create(
        #     document_id=du.document_id,
        #     action=DocumentState.created,
        #     action_msg=f"Document <{dc.document_filename} created by user {cur_user.user_name}> ."
        # )
        # doc_audit = get_document_audit_service.create(db, audit_log)

        return result
    except json.JSONDecodeError as jde:
        raise InternalServerException("Malformed JSON found as output of the file!")
    except HTTPException as ex:
        raise InternalServerException(ex.detail)
    except Exception as ex:
        logger.exception(ex)
        raise InternalServerException("File Reading Error")
