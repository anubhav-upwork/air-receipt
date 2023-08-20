from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def validate_password(password: str, pwhash: str):
    return pwd_context.verify(password, pwhash)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# from werkzeug.security import generate_password_hash, check_password_hash
#
#
# def hash_password(password: str) -> str:
#     """Create hashed password."""
#     return generate_password_hash(
#         password,
#         method='sha256'
#     )
#
#
# def validate_password(password: str, pwhash: str) -> bool:
#     """Check hashed password."""
#     return check_password_hash(pwhash, password)
