# from fastapi import FastAPI
#
# # sqlalchemy
# from sqlalchemy import text
#
# # assuming that the users directory is within the modules directory,
# # and the models.py file is within the users directory.
# from app.db.dbconnect import engine, Base
# from app.models.user.user_info import User_Info
# from app.models.user.user_types import User_Types
# from app.models.user.user_roles import User_Roles
# # from app.models.documents.document_user import Document_User
# # from app.models.documents.document_category import Document_Category
# # from app.models.documents.document_class import Document_Class
#
# # from app.modules.users import routes as user_routes
# # from app.modules.todos import routes as todo_routes
#
# # # This will create all the tables in the database
# Base.metadata.create_all(bind=engine)
#
# # app = FastAPI()
#
# # # Include routes for each group of endpoints
# # app.include_router(user_routes.router, prefix="/users", tags=["users"])
# # app.include_router(todo_routes.router, prefix="/todos", tags=["todos"])
#
#
# # # Check if database is functional
# # @app.on_event("startup")
# # async def startup_event():
# #     # create a new database session for the startup event
# #     session = SessionLocal()
#
# #     # Test database connection
# #     try:
# #         # execute a query to check if the connection is successful
# #         session.execute(text("SELECT 1"))
# #     except Exception as e:
# #         print(f"An error occurred: {e}")
# #     finally:
# #         # close the session
# #         session.close()
#
#
# # @app.get("/")
# # def app_root():
# #     return {"Hello": "World"}

from app.app import create_app

app = create_app()
