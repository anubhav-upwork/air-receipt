# from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
#
# import sqlalchemy
# from fastapi.encoders import jsonable_encoder
# from pydantic import BaseModel
# from sqlalchemy.orm import Session
# from sqlalchemy.exc import IntegrityError
# from starlette.exceptions import HTTPException
#
# from app.db.dbconnect import Base
#
# ModelType = TypeVar("ModelType", bound=Base)
# CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
# UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
#
#
# class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
#     def __init__(self, model: Type[ModelType]):
#         self.model = model
#
#     def get(self, db: Session, id: Any) -> Optional[ModelType]:
#         obj: Optional[ModelType] = db.query(self.model).get(id)
#         if obj is None:
#             raise HTTPException(status_code=404, detail="Not Found")
#         return obj
#
#     def get_multi(
#             self, db: Session, *, skip: int = 0, limit: int = 100
#     ) -> List[ModelType]:
#         return db.query(self.model).offset(skip).limit(limit).all()
#
#     def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
#         obj_in_data = jsonable_encoder(obj_in)
#         db_obj: ModelType = self.model(**obj_in_data)  # type: ignore
#         db.add(db_obj)
#         try:
#             db.commit()
#         except sqlalchemy.exc.IntegrityError as e:
#             db.rollback()
#             if "duplicate key" in str(e):
#                 raise HTTPException(status_code=409, detail="Conflict Error")
#             else:
#                 raise e
#         return db_obj
#
#     def update(
#             self,
#             db: Session,
#             *,
#             db_obj: ModelType,
#             obj_in: Union[UpdateSchemaType, Dict[str, Any]]
#     ) -> ModelType:
#         obj_data = jsonable_encoder(db_obj)
#         if isinstance(obj_in, dict):
#             update_data = obj_in
#         else:
#             update_data = obj_in.dict(exclude_unset=True)
#         for field in obj_data:
#             if field in update_data:
#                 setattr(db_obj, field, update_data[field])
#         db.add(db_obj)
#         db.commit()
#         db.refresh(db_obj)
#         return db_obj
#
#     def remove(self, db: Session, *, id: int) -> ModelType:
#         obj = db.query(self.model).get(id)
#         db.delete(obj)
#         db.commit()
#         return obj
