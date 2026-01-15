from sqlmodel import Session
from ..config.database import engine
from contextlib import contextmanager


@contextmanager
def get_db_session():
    """
    Dependency to get a database session.
    """
    with Session(engine) as session:
        yield session