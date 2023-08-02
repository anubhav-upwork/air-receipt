from fastapi import FastAPI
from app.db.dbconnect import engine, Base
from fastapi.responses import JSONResponse
from app.models.user.user_roles import User_Roles
from app.models.user.user_types import User_Types
from app.models.user.user_info import User_Info

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

    from app.routes.user import user_role_route
    from app.routes.user import user_type_route

    app.include_router(user_role_route.router)
    app.include_router(user_type_route.router)
    # app.include_router(stores.router)
    return app
