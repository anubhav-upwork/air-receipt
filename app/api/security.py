from werkzeug.security import generate_password_hash, check_password_hash


def hash_password(password: str) -> str:
    """Create hashed password."""
    return generate_password_hash(
        password,
        method='sha256'
    )


def validate_password(password: str, pwhash: str) -> bool:
    """Check hashed password."""
    return check_password_hash(pwhash, password)
