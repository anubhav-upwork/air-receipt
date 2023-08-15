from typing import Generator, Optional

from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from pydantic import BaseModel
from sqlalchemy.orm.session import Session

from app.core.auth import oauth2_scheme, JWT_SECRET, ALGORITHM
# from app.core.config import settings
from app.db.session import SessionLocal
from app.models.user.user_info import User_Info
from app import crud


class TokenData(BaseModel):
    username: Optional[str] = None


def get_db() -> Generator:
    db = SessionLocal()
    db.current_user_id = None
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User_Info:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[ALGORITHM],
            options={"verify_aud": False},
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = db.query(User_Info).filter(User_Info.user_email == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user


def get_current_active_superuser(
    current_user: User_Info = Depends(get_current_user),
) -> User_Info:
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
