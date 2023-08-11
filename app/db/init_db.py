import logging
from sqlalchemy.orm import Session
from app.crud import user
from app.schemas.user.user_roles import UserRole_Create
from app.schemas.user.user_types import UserType_Create
# from app.crud.user.user_types import User_Types
# from app.crud.user.user_roles import User_Roles
from app.db import base  # noqa: F401

# Data
from app.db_data.user_roles_data import USER_ROLES_DATA
from app.db_data.user_types_data import USER_TYPES_DATA

logger = logging.getLogger(__name__)


# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    # populate user roles
    for role in USER_ROLES_DATA:
        obj = UserRole_Create(
            user_role=role["user_role"],
            user_access_level=role["user_access_level"]
        )
        try:
            user.get_user_role_service.create(db, obj)
        except Exception as e:
            logger.warning(f"Role already exists{e}")


#
# def init_db(db: Session) -> None:
#     # Tables should be created with Alembic migrations
#     # But if you don't want to use migrations, create
#     # the tables un-commenting the next line
#     # Base.metadata.create_all(bind=engine)
#     if settings.FIRST_SUPERUSER:
#         user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
#         if not user:
#             user_in = schemas.UserCreate(
#                 full_name="Initial Super User",
#                 email=settings.FIRST_SUPERUSER,
#                 is_superuser=True,
#                 password=settings.FIRST_SUPERUSER_PW,
#             )
#             user = crud.user.create(db, obj_in=user_in)  # noqa: F841
#         else:
#             logger.warning(
#                 "Skipping creating superuser. User with email "
#                 f"{settings.FIRST_SUPERUSER} already exists. "
#             )
#         if not user.recipes:
#             for recipe in RECIPES:
#                 recipe_in = schemas.RecipeCreate(
#                     label=recipe["label"],
#                     source=recipe["source"],
#                     url=recipe["url"],
#                     submitter_id=user.id,
#                 )
#                 crud.recipe.create(db, obj_in=recipe_in)
#     else:
#         logger.warning(
#             "Skipping creating superuser.  FIRST_SUPERUSER needs to be "
#             "provided as an env variable. "
#             "e.g.  FIRST_SUPERUSER=admin@api.coursemaker.io"
#         )
