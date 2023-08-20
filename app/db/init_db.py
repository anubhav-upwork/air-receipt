from app.core.airlogger import logger
from sqlalchemy.orm import Session

from app.crud import user
from app.schemas.user.user_roles import UserRole_Create
from app.schemas.user.user_types import UserType_Create
from app.schemas.user.user_info import UserInfoSuper_Create

from app.crud import document
from app.schemas.document.document_class import DocumentClass_Create
from app.schemas.document.document_category import DocumentCategory_Create

from app.db.session import engine
from app.db.base_class import Base

# USER Data
from app.db_data.user_roles_data import USER_ROLES_DATA
from app.db_data.user_types_data import USER_TYPES_DATA
from app.db_data.first_user_data import FIRST_USER_DATA

# DOCUMENT Data
from app.db_data.document_class_data import DOCUMENT_CLASS_DATA
from app.db_data.document_category_data import DOCUMENT_CATEGORY_DATA


# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28


def init_db(db: Session) -> bool:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    Base.metadata.create_all(bind=engine)

    # populate user roles
    for role in USER_ROLES_DATA:
        obj = UserRole_Create(
            user_role=role["user_role"],
            user_access_level=role["user_access_level"]
        )
        try:
            user.get_user_role_service.create(db, obj)
            logger.info(f"Role Created {obj}")
        except Exception as e:
            logger.warning(f"Role already exists{e}")
            # return False

    # populate user types
    for utype in USER_TYPES_DATA:
        obj = UserType_Create(
            user_type=utype["user_type"],
            usage_limit_days=utype["usage_limit_days"]
        )

        try:
            user.get_user_type_service.create(db, obj)
            logger.info(f"User Type Created {obj}")
        except Exception as e:
            logger.warning(f"User Type already exists{e}")
            # return False

    # create first user
    obj_first_user = UserInfoSuper_Create(
        user_name=FIRST_USER_DATA["user_name"],
        user_email=FIRST_USER_DATA["user_email"],
        user_mobile=FIRST_USER_DATA["user_mobile"],
        user_location=FIRST_USER_DATA["user_location"],
        user_password=FIRST_USER_DATA["user_password"],
        user_role=FIRST_USER_DATA["user_role"],
        user_type=FIRST_USER_DATA["user_type"],
        user_credit=FIRST_USER_DATA["user_credit"],
        user_is_superuser=FIRST_USER_DATA["user_is_superuser"],
        user_is_deleted=FIRST_USER_DATA["user_is_deleted"],
        user_is_active=FIRST_USER_DATA["user_is_active"]
    )

    try:
        user.get_user_info_service.create_super_user(db, obj_first_user)
        logger.info(f"Initial User Created {obj_first_user}")
    except Exception as e:
        logger.warning(f"Initial User already exists{e}")
        return False

    # Populate Document Category Data
    for docCat in DOCUMENT_CATEGORY_DATA:
        obj = DocumentCategory_Create(
            category=docCat["category"],
            category_code=docCat["category_code"]
        )

        try:
            document.get_document_category_service.create(db, obj)
            logger.info(f"Document Category Created {obj}")
        except Exception as e:
            logger.warning(f"Document Category already exists{e}")
            # return False

    for docClass in DOCUMENT_CLASS_DATA:
        obj = DocumentClass_Create(
            doc_class=docClass["doc_class"],
            doc_class_code=docClass["doc_class_code"]
        )
        try:
            document.get_document_class_service.create(db, obj)
            logger.info(f"Document Class Created {obj}")
        except Exception as e:
            logger.warning(f"Document Class already exists{e}")
            # return False


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
