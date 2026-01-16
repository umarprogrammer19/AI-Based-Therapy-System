from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional
from sqlalchemy import Column, DateTime
from enum import Enum


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"


class UserBase(SQLModel):
    """
    Base class for User with shared attributes.
    """
    email: str = Field(..., unique=True, nullable=False, max_length=255)
    username: str = Field(..., unique=True, nullable=False, max_length=100)
    full_name: Optional[str] = Field(default=None, max_length=255)
    role: UserRole = Field(default=UserRole.USER)
    is_active: bool = Field(default=True)


class User(UserBase, table=True):
    """
    User model representing application users.
    """
    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    hashed_password: str = Field(..., nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime(timezone=True)))
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column=Column(DateTime(timezone=True)))
    last_login_at: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True)))


class UserCreate(UserBase):
    """
    Schema for creating a new user.
    """
    password: str = Field(..., min_length=8)


class UserRead(UserBase):
    """
    Schema for reading user data (without password).
    """
    id: UUID
    created_at: datetime
    updated_at: datetime
    last_login_at: Optional[datetime]


class UserUpdate(SQLModel):
    """
    Schema for updating user data.
    """
    email: Optional[str] = None
    username: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[UserRole] = None


class UserLogin(SQLModel):
    """
    Schema for user login.
    """
    username: str
    password: str


class Token(SQLModel):
    """
    Schema for authentication token.
    """
    access_token: str
    token_type: str = "bearer"


class TokenData(SQLModel):
    """
    Schema for token data.
    """
    username: Optional[str] = None
    user_id: Optional[UUID] = None
    role: Optional[UserRole] = None