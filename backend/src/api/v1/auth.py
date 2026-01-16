from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from ...services.auth import auth_service
from ...services.user import user_service
from ...models.user import UserCreate, UserLogin, Token, UserRead
from ...api.async_deps import get_async_db_session
from ...config.settings import settings


router = APIRouter(tags=["auth"])


@router.post("/register", response_model=UserRead)
async def register_user(
    user_create: UserCreate,
    session: AsyncSession = Depends(get_async_db_session)
):
    """
    Register a new user.
    """
    # Check if user already exists
    existing_user = await user_service.get_user_by_username(session, user_create.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    existing_email = await user_service.get_user_by_email(session, user_create.email)
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create the user
    user = await user_service.create_user(session, user_create)
    return user


@router.post("/login", response_model=Token)
async def login_user(
    user_login: UserLogin,
    session: AsyncSession = Depends(get_async_db_session)
):
    """
    Login a user and return access token.
    """
    user = await auth_service.authenticate_user(
        session, user_login.username, user_login.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Update last login time
    user.last_login_at = datetime.utcnow()
    session.add(user)
    await session.commit()
    await session.refresh(user)  # Refresh to ensure all fields are loaded

    # Create access token
    access_token_expires = timedelta(minutes=auth_service.access_token_expire_minutes)
    access_token = auth_service.create_access_token(
        data={
            "sub": user.username,
            "user_id": str(user.id),
            "role": user.role.value
        },
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=UserRead)
async def read_users_me(
    current_user: UserRead = Depends(auth_service.get_current_user_dependency())
):
    """
    Get current user info.
    """
    return current_user