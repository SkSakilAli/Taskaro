from pydantic import BaseModel


class Base(BaseModel):
    pass


class Create_Task(Base):
    title: str


class User(Base):
    id: int | None = None
    name: str
    email: str
    is_supervisor: bool = False
    password: str


class Add_Subordinate(Base):
    email: str
