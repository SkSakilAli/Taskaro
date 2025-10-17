from model.schema import Supervisor, Users
from model.config import SessionLocal
from sqlalchemy import select
from model.user import get_user_db
from fastapi import HTTPException


def check_if_supervisor(user_id):
    with SessionLocal() as session:
        user = session.get(Users, user_id)
        if user.is_supervisor:
            return True
        else:
            return False


def add_subordinate_db(user_id: int, subordinate_email: str):
    with SessionLocal() as session:
        statement = select(Users).where(Users.email == subordinate_email)
        subordinate_db = session.scalar(statement)
        supervisor_subordinate = Supervisor(
            supervisor=user_id, subordinate=subordinate_db.id
        )
        session.add(supervisor_subordinate)
        session.commit()
        session.refresh(supervisor_subordinate)
        return supervisor_subordinate


def get_subordinate_db(user_id):
    with SessionLocal() as session:
        statement = select(Supervisor).where(Supervisor.supervisor == user_id)
        subordinates_id = session.scalars(statement).all()
        subordinates = {}
        # return subordinates_id
        for data in subordinates_id:
            user = get_user_db(data.subordinate)
            subordinates.update({user.id: user.name})
        return subordinates


def check_supervisor_subordinate_relation(supervisor_id: int, subordinate_id: int):
    if not check_if_supervisor(supervisor_id):
        raise HTTPException(status_code=401, detail="Not a Supervisor")
    else:
        subordinates_all = get_subordinate_db(supervisor_id)
        for data in subordinates_all.keys():
            if data == subordinate_id:
                return data
        raise HTTPException(status_code=400, detail="Not authorized")
