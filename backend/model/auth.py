from passlib.context import CryptContext
from model.schema import Users, RefreshToken
from model.config import SessionLocal
from sqlalchemy import select

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str):
    hashed = pwd_context.hash(password)
    return hashed


def create_user(
    user_name: str,
    user_email: str,
    user_password: str,
    is_supervisor: bool = False,
):
    hashed_user_password = hash_password(user_password)
    with SessionLocal() as session:
        user = Users(
            name=user_name,
            email=user_email,
            password=hashed_user_password,
            is_supervisor=is_supervisor,
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


def get_user_by_id(user_id: int):
    with SessionLocal() as session:
        user = session.get_one(Users, user_id)
        return user


def get_user_by_email(user_email: str):
    with SessionLocal() as session:
        statement = select(Users).where(Users.email == user_email)
        user = session.scalar(statement)
        return user


def verify_password(user_email: str, user_password):
    user = get_user_by_email(user_email)
    return pwd_context.verify(user_password, user.password)


def add_refresh_token(token_given, created_at_given, expires_at_given, user_id_given):
    with SessionLocal() as session:
        # Checking if refreshToken already exist if so removing it thus allowing only one device signin per user
        statement = select(RefreshToken).where(RefreshToken.user_id == user_id_given)
        refresh_token_if_exist = session.scalar(statement)
        if refresh_token_if_exist:
            session.delete(refresh_token_if_exist)

        refresh_token = RefreshToken(
            user_id=user_id_given,
            token=token_given,
            is_revoked=False,
            created_at=created_at_given,
            expires_at=expires_at_given,
        )
        session.add(refresh_token)
        session.commit()
        session.refresh(refresh_token)
        return refresh_token


def get_refresh_token_db(refresh_token):
    with SessionLocal() as session:
        statement = select(RefreshToken).where(RefreshToken.token == refresh_token)
        token = session.scalar(statement)
        return token
