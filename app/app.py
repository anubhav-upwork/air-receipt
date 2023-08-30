from fastapi import FastAPI
from app.db.session import engine, SessionLocal
from app.db.base_class import Base
from fastapi.responses import JSONResponse

# sqlalchemy
from sqlalchemy import text

# logger
from app.core.airlogger import logger

from app.models.user.user_roles import User_Roles
from app.models.user.user_types import User_Types
from app.models.user.user_info import User_Info
from app.models.user.user_login import User_Login
from app.models.user.user_action_audit import User_Audit_Trail
from app.models.documents.document_category import Document_Category
from app.models.documents.document_class import Document_Class
from app.models.documents.document_user import Document_User
from app.models.documents.document_action_audit import Document_Audit_Trail

# Base.metadata.drop_all(engine)
# Base.metadata.create_all(bind=engine)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Air Receipt",
        description="Simple AI solution for your Invoice Digitization.",
        version="1.0",
    )

    # Check if database is functional
    @app.on_event("startup")
    async def startup_event():
        # create a new database session for the startup event
        session = SessionLocal()

        # Test database connection
        try:
            # execute a query to check if the connection is successful
            session.execute(text("SELECT 1"))
            logger.info(f"Checking Connection with Database Done ")
        except Exception as e:
            logger.error(f"An error occurred: {e}")
        finally:
            # close the session
            logger.info(f"Closing Connection with Database xxx")
            session.close()

    @app.get("/health")
    async def health() -> str:
        return "ok"

    @app.get("/")
    def app_root():
        return {"Deck": "Air Receipt - Invoice Digitization"}

    @app.exception_handler(Exception)
    def validation_exception_handler(request, err):
        base_error_message = f"Failed to execute: {request.method}: {request.url}"
        return JSONResponse(status_code=400, content={"message": f"{base_error_message}. Detail: {err}"})

    from app.api.api_v1.endpoints.user import user_role_route, user_type_route, user_info_route
    from app.api.api_v1.endpoints.document import document_class_route, document_category_route, document_user_route
    from app.api.api_v1.endpoints.user import user_auth

    # User Routes
    app.include_router(user_role_route.router)
    app.include_router(user_type_route.router)
    app.include_router(user_info_route.router)
    app.include_router(user_auth.router)

    # Document Routes
    app.include_router(document_class_route.router)
    app.include_router(document_category_route.router)
    app.include_router(document_user_route.router)

    return app
