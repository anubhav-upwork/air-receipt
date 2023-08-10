from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session

SQLALCHEMY_DATABASE_URL = "mysql://anubhav:anubhav123@localhost:3307/air"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    echo=False)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


