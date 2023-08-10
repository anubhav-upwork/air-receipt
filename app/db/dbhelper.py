
# from typing import Generator
# from app.db.dbconnect import scoped_session, create_session
#
#
# def get_session() -> Generator[scoped_session, None, None]:
#     Session = create_session()
#     try:
#         yield Session
#     finally:
#         Session.remove()
#
# # Dependency
# # def get_db():
# #     db = SessionLocal()
# #     try:
# #         yield db
# #     finally:
# #         db.close()
