from model.config import SessionLocal, engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, ForeignKey, DateTime
import datetime as dt


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    is_supervisor: Mapped[bool] = mapped_column(Boolean)
    tasks: Mapped[list["Tasks"]] = relationship(
        "Tasks", back_populates="user", cascade="all, delete"
    )
    password: Mapped[str] = mapped_column(String, nullable=False)


class Tasks(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE")
    )
    user: Mapped["Users"] = relationship("Users", back_populates="tasks")
    title: Mapped[str] = mapped_column(String, nullable=False)

    assigned_by: Mapped[int] = mapped_column(
        Integer, ForeignKey("supervisors.supervisor"), nullable=True
    )


class Supervisor(Base):
    __tablename__ = "supervisors"
    supervisor: Mapped[Users] = mapped_column(
        Integer, ForeignKey("users.id"), primary_key=True
    )
    subordinate: Mapped[list["Users"]] = mapped_column(Integer, ForeignKey("users.id"))


class RefreshToken(Base):
    __tablename__ = "refreshToken"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    token: Mapped[str] = mapped_column(String, nullable=False)
    is_revoked: Mapped[bool] = mapped_column(Boolean)
    created_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True))
    expires_at: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True))


def create_db():
    Base.metadata.create_all(engine)


create_db()
