import logging
from datetime import datetime, timedelta
from typing import MutableMapping, List, Union, Any

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from sqlalchemy.orm.session import Session

from app.core.security import validate_password
from app.models.user.user_info import User_Info

logger = logging.getLogger(__name__)

API_V1_STR: str = "/api/v1"
JWT_SECRET: str = "a$$nubh@v_airalpha+$%%receipt+17JulvyTwo1000&23"
JWT_REFRESH_SECRET_KEY: str = "charlie$%^&&saved_+the-d8123#anubhav#"
ALGORITHM: str = "HS256"

# 60 minutes * 24 hours * 8 days = 8 days
ACCESS_TOKEN_EXPIRE_MINUTES: int = 10  # 10 minutes
REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

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


def create_refresh_token(sub: Union[str, Any], expires_delta: timedelta = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expires_delta, "iat": datetime.utcnow(), "sub": str(sub)}
    return jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, algorithm=ALGORITHM)

