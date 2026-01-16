from datetime import datetime, timedelta
from typing import Optional
import bcrypt
from jose import JWTError, jwt
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from ..models.user import User, UserLogin, TokenData
from ..config.settings import settings
from ..api.async_deps import get_async_db_session
from uuid import UUID


class AuthService:
    """
    Service class for handling user authentication and authorization.
    """

    def __init__(self):
        self.secret_key = settings.secret_key
        self.algorithm = settings.algorithm
        self.access_token_expire_minutes = settings.access_token_expire_minutes
        self.oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a plain password against a hashed password.
        """
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

    def get_password_hash(self, password: str) -> str:
        """
        Hash a password using bcrypt.
        """
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Create a JWT access token.
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt

    async def authenticate_user(self, session: AsyncSession, username: str, password: str) -> Optional[User]:
        """
        Authenticate a user by username and password.
        """
        result = await session.execute(select(User).where(User.username == username))
        user = result.scalar_one_or_none()

        if not user or not self.verify_password(password, user.hashed_password):
            return None

        return user

    def decode_token(self, token: str) -> Optional[TokenData]:
        """
        Decode a JWT token and return token data.
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            username: str = payload.get("sub")
            user_id: str = payload.get("user_id")
            role: str = payload.get("role")

            if username is None or user_id is None:
                return None

            token_data = TokenData(username=username, user_id=UUID(user_id), role=role)
            return token_data
        except JWTError:
            return None

    def get_current_user_dependency(self):
        """
        Creates a dependency function that extracts user from token.
        """
        async def get_current_user(
            token: str = Depends(self.oauth2_scheme),
            session: AsyncSession = Depends(get_async_db_session)
        ) -> User:
            credentials_exception = HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

            token_data = self.decode_token(token)
            if token_data is None:
                raise credentials_exception

            result = await session.execute(select(User).where(User.id == token_data.user_id))
            user = result.scalar_one_or_none()

            if user is None:
                raise credentials_exception

            return user

        return get_current_user


# Global instance
auth_service = AuthService()