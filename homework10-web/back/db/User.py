from typing import Tuple

from sqlalchemy import String, Integer, select
from sqlalchemy import Column
from sqlalchemy.orm import relationship

from db.engine_generator import Base


class User(Base):  # type:ignore
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    username = Column("username", String(50), unique=True)
    password = Column("password", String(127))
    notes = relationship("Note")

    @staticmethod
    def get_by_username(username: str, sessionBuilder):
        with sessionBuilder() as session:
            users = session.execute(select(User).where(User.username == username)).fetchall()
            if users:
                return users[0].User

    @staticmethod
    def create_user(username: str, password: str, sessionBuilder) -> Tuple[int, str, str]:
        with sessionBuilder() as session:
            user = User(username=username, password=password)
            session.add(user)
            session.commit()

            user = session.execute(select(User).where(User.username == username)).fetchall()[0].User
            return user.id, user.username, user.password
