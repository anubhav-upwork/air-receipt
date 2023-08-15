from fastapi import FastAPI
from app.db.session import engine
from app.db.base_class import Base
from fastapi.responses import JSONResponse
from app.models.user.user_roles import User_Roles
from app.models.user.user_types import User_Types
from app.models.user.user_info import User_Info
from app.models.user.user_login import User_Login
from app.models.user.user_action_audit import User_Audit_Trail
from app.models.documents.document_category import Document_Category
from app.models.documents.document_class import  Document_Class
from app.models.documents.document_user import Document_User
from app.models.documents.document_action_audit import Document_Audit_Trail

# Base.metadata.drop_all(engine)
Base.metadata.create_all(bind=engine)


def create_app() -> FastAPI:
    app = FastAPI(
        title="Air Receipt",
        description="Simple AI solution for your Invoice Digitization.",
        version="1.0",
    )

    @app.get("/health")
    async def health() -> str:
        return "ok"

    @app.exception_handler(Exception)
    def validation_exception_handler(request, err):
        base_error_message = f"Failed to execute: {request.method}: {request.url}"
        return JSONResponse(status_code=400, content={"message": f"{base_error_message}. Detail: {err}"})

    from app.api.api_v1.endpoints.user import user_role_route, user_type_route, user_info_route
    # from app.api.api_v1.endpoints.user import user_type_route
    # from app.api.api_v1.endpoints.user import user_info_route

    from app.api.api_v1.endpoints.document import document_class_route, document_category_route
    from app.api.api_v1.endpoints.user import user_auth
    app.include_router(user_role_route.router)
    app.include_router(user_type_route.router)
    app.include_router(user_info_route.router)
    app.include_router(document_class_route.router)
    app.include_router(document_category_route.router)
    app.include_router(user_auth.router)

    # app.include_router(stores.router)
    return app
