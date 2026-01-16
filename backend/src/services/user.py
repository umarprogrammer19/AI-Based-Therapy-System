from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from typing import Optional
from uuid import UUID
from ..models.user import User, UserCreate, UserUpdate
from ..services.auth import auth_service


class UserService:
    """
    Service class for handling user-related operations.
    """

    async def create_user(self, session: AsyncSession, user_create: UserCreate) -> User:
        """
        Create a new user.
        """
        # Hash the password
        hashed_password = auth_service.get_password_hash(user_create.password)

        # Create the user object
        db_user = User(
            email=user_create.email,
            username=user_create.username,
            full_name=user_create.full_name,
            role=user_create.role,
            hashed_password=hashed_password
        )

        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)

        return db_user

    async def get_user_by_id(self, session: AsyncSession, user_id: UUID) -> Optional[User]:
        """
        Get a user by ID.
        """
        result = await session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_user_by_username(self, session: AsyncSession, username: str) -> Optional[User]:
        """
        Get a user by username.
        """
        result = await session.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    async def get_user_by_email(self, session: AsyncSession, email: str) -> Optional[User]:
        """
        Get a user by email.
        """
        result = await session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def update_user(self, session: AsyncSession, user_id: UUID, user_update: UserUpdate) -> Optional[User]:
        """
        Update a user.
        """
        db_user = await self.get_user_by_id(session, user_id)
        if not db_user:
            return None

        # Update the fields that are provided
        update_data = user_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)

        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)

        return db_user

    async def delete_user(self, session: AsyncSession, user_id: UUID) -> bool:
        """
        Delete a user.
        """
        db_user = await self.get_user_by_id(session, user_id)
        if not db_user:
            return False

        await session.delete(db_user)
        await session.commit()

        return True

    async def get_all_users(self, session: AsyncSession, skip: int = 0, limit: int = 100):
        """
        Get all users with pagination.
        """
        result = await session.execute(select(User).offset(skip).limit(limit))
        return result.scalars().all()


# Global instance
user_service = UserService()