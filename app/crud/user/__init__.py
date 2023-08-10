# _*_ coding: utf-8 _*_
"""
  Created by Anubhav Rohatgi on 24/07/2023.
"""
__author__ = 'Anubhav Rohatgi'

from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.dbhelper import get_session

from .user_roles import userRoleCrud
from .user_types import userTypeCrud
from .user_info import userInfoCrud


# def get_user_role_service(db_session: Session = Depends(get_session)) -> UserRoleService:
#     return UserRoleService(db_session)
#
#
# def get_user_type_service(db_session: Session = Depends(get_session)) -> UserTypeService:
#     return UserTypeService(db_session)
#
#
# def get_user_info_service(db_session: Session = Depends(get_session)) -> UserInfoService:
#     return UserInfoService(db_session)
