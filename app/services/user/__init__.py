# _*_ coding: utf-8 _*_
"""
  Created by Anubhav Rohatgi on 24/07/2023.
"""
__author__ = 'Anubhav Rohatgi'

from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.dbconnect import get_session

from .user_roles import UserRoleService


def get_user_role_service(db_session: Session = Depends(get_session)) -> UserRoleService:
    return UserRoleService(db_session)
