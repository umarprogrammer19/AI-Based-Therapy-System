import logging
from typing import Optional
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from ..config.settings import settings


# Set up logging
logger = logging.getLogger(__name__)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against a hashed password.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Generate a hash for a plaintext password.
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    Create a JWT access token with expiration.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


def verify_access_token(token: str):
    """
    Verify and decode a JWT access token.
    """
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload
    except JWTError as e:
        logger.error(f"Token verification failed: {e}")
        return None


def validate_api_key(api_key: str) -> bool:
    """
    Validate the provided API key against the configured key.
    """
    if not api_key:
        return False

    if not settings.hugging_face_api_key:
        logger.warning("API key validation failed: No HUGGING_FACE_API_KEY configured")
        return False

    return api_key == settings.hugging_face_api_key


def mask_sensitive_data(data: str) -> str:
    """
    Mask sensitive data like API keys for logging purposes.
    """
    if not data:
        return data

    # Mask everything except the first 3 and last 3 characters
    if len(data) <= 6:
        return "*" * len(data)

    return data[:3] + "*" * (len(data) - 6) + data[-3:]