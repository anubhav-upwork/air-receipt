from functools import lru_cache
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

SQLALCHEMY_DATABASE_URL = "mysql://anubhav:anubhav123@localhost:3307/air"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, pool_pre_ping=True)


@lru_cache
def create_session() -> scoped_session:
    Session = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=engine)
    )
    return Session


Base = declarative_base()


# Test database connection: If it replies back a (1,) the connection was successful
def test_connection():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        return result.fetchone()

# engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
#
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
# Base = declarative_base()
#
#
# # Test database connection: If it replies back a (1,) the connection was successful
# def test_connection():
#     with engine.connect() as connection:
#         result = connection.execute(text("SELECT 1"))
#         return result.fetchone()
