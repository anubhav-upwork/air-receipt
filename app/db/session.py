from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# SQLALCHEMY_DATABASE_URL = "mysql://anubhav:anubhav123@localhost:3307/new_schema"


engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    pool_pre_ping=True,
    echo=False)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


