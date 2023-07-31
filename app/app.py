from fastapi import FastAPI
from app.db.dbconnect import engine, Base

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

    from app.routes.user import user_role_route

    app.include_router(user_role_route.router)
    # app.include_router(products.router)
    # app.include_router(stores.router)
    return app
