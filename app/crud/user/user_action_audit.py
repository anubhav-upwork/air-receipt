import sqlalchemy
from typing import Optional

from sqlalchemy.orm import Session
from app.models.user.user_action_audit import User_Audit_Trail, User_Action
from app.schemas.user.user_action_audit import UserAuditTrail_Create, UserAuditTrail_Update, UserAuditTrail
from app.crud.base import BaseService
from sqlalchemy.exc import IntegrityError
from starlette.exceptions import HTTPException


class UserActionAuditService(BaseService[User_Audit_Trail, UserAuditTrail_Create, UserAuditTrail_Update]):

    def create(self, db_session: Session, obj_in: UserAuditTrail_Create) -> User_Audit_Trail:
        db_obj = User_Audit_Trail(
            user_id=obj_in.user_id,
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


get_user_action_audit_service = UserActionAuditService(User_Audit_Trail)
