from typing import Any, Generic, List, Optional, Type, TypeVar

import sqlalchemy
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from starlette.exceptions import HTTPException

from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db_session: Session, _id: Any) -> Optional[ModelType]:
        obj: Optional[ModelType] = db_session.query(self.model).get(_id)
        if obj is None:
            raise HTTPException(status_code=404, detail="Not Found")
        return obj

    def list(self, db_session: Session) -> List[ModelType]:
        objs: List[ModelType] = db_session.query(self.model).all()
        return objs

    def create(self, db_session: Session, obj: CreateSchemaType) -> ModelType:
        db_obj: ModelType = self.model(**obj.dict())
        db_session.add(db_obj)
        try:
            db_session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            db_session.rollback()
            if "duplicate key" in str(e):
                raise HTTPException(status_code=409, detail="Conflict Error")
            else:
                raise e
        return db_obj

    def update(self, db_session: Session, _id: Any, obj: UpdateSchemaType) -> Optional[ModelType]:
        db_obj = self.get(db_session, _id)
        for column, value in obj.model_dump(exclude_unset=True).items():
            setattr(db_obj, column, value)
        db_session.commit()
        return db_obj

    def delete(self, db_session: Session, _id: Any) -> Optional[ModelType]:
        db_obj = db_session.query(self.model).get(_id)
        db_session.delete(db_obj)
        db_session.commit()
        return db_obj
