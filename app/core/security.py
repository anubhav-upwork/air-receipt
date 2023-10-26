from passlib.context import CryptContext

# String Hasher and Password Validator

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def validate_password(password: str, pwhash: str):
    return pwd_context.verify(password, pwhash)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)
