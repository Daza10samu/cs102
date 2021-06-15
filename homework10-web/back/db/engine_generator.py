import typing

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()


def generate_engine(
    url: str = "postgresql+pg8000://maindb_hw10:maindb_hw10@db_hw10:5432/maindb_hw10",
) -> Engine:
    engine = create_engine(url, echo=True)
    from .User import User
    from .Note import Note

    Base.metadata.create_all(engine)

    return engine
