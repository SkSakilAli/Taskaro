from model.schema import Tasks
from model.config import SessionLocal
from sqlalchemy import select


def add_task_db(
    user_id_given: int, title_given: str, assigned_by_given: int | None = None
):
    with SessionLocal() as session:
        if not assigned_by_given:
            task = Tasks(user_id=user_id_given, title=title_given)
        else:
            task = Tasks(
                user_id=user_id_given, title=title_given, assigned_by=assigned_by_given
            )
        session.add(task)
        session.commit()
        session.refresh(task)
        return task


def get_task_by_user_id(user_id: int):
    with SessionLocal() as session:
        statement = select(Tasks).where(Tasks.user_id == user_id)
        tasks = session.scalars(statement).all()
        return tasks


def mark_as_complete_db(task_id):
    with SessionLocal() as session:
        task = session.get_one(Tasks, task_id)
        task.status = True
        session.commit()
        session.refresh(task)
        return task
