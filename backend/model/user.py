from model.schema import Users
from model.config import SessionLocal
from sqlalchemy import select


def create_user_db(user_name, user_email, user_password):
    with SessionLocal() as session:
        user = Users(name=user_name, email=user_email, password=user_password)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


def get_user_db(user_id):
    with SessionLocal() as session:
        user = session.get_one(Users, user_id)
        return user
