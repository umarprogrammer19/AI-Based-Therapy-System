from sqlmodel import Session
from ..database.connection import engine


def get_db_session():
    """
    Dependency to get a database session.
    """
    with Session(engine) as session:
        yield session