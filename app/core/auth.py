import logging
from typing import Optional, MutableMapping, List, Union, Any, Type
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm.session import Session
from jose import jwt

from app.models.user.user_info import User_Info
from app.core.security import validate_password

logger = logging.getLogger(__name__)

API_V1_STR: str = "/api/v1"
JWT_SECRET: str = "TEST_SECRET_DO_NOT_USE_IN_PROD"
ALGORITHM: str = "HS256"

# 60 minutes * 24 hours * 8 days = 8 days
ACCESS_TOKEN_EXPIRE_MINUTES: int = 10

JWTPayloadMapping = MutableMapping[
    str, Union[datetime, bool, str, List[str], List[int]]
]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def authenticate(
    *,
    email: str,
    password: str,
    db: Session,
) -> User_Info | None:
    user = db.query(User_Info).filter(User_Info.user_email == email).first()
    if not user:
        logger.warning("No matching user found, authentication failed!")
        return None
    if not validate_password(password, user.user_password):
        logger.warning("Authentication failed!")
        return None
    return user


def create_access_token(*, sub: str) -> str:
    return _create_token(
        token_type="access_token",
        lifetime=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub,
    )


def _create_token(
    token_type: str,
    lifetime: timedelta,
    sub: str,
) -> str:
    payload = {}
    expire = datetime.utcnow() + lifetime
    payload["type"] = token_type

    # https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.3
    # The "exp" (expiration time) claim identifies the expiration time on
    # or after which the JWT MUST NOT be accepted for processing
    payload["exp"] = expire

    # The "iat" (issued at) claim identifies the time at which the
    # JWT was issued.
    payload["iat"] = datetime.utcnow()

    # The "sub" (subject) claim identifies the principal that is the
    # subject of the JWT
    payload["sub"] = str(sub)
    return jwt.encode(payload, JWT_SECRET, algorithm=ALGORITHM)
