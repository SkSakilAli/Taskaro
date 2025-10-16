from model.auth import (
    create_user,
    get_user_by_id,
    verify_password,
    get_user_by_id,
    add_refresh_token,
    get_refresh_token_db,
)
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, tzinfo, timezone
from jose import jwt
from fastapi import HTTPException
from fastapi import Depends
from typing import Annotated
from dotenv import load_dotenv
import os

load_dotenv()


Oauth_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


Secret_Key = os.getenv("SECRET_KEY")
Algorithm = os.getenv("TOKEN_ALGORITHM")


def authenticate_user(token: Annotated[str, Depends(Oauth_scheme)]):
    access_token = jwt.decode(token, Secret_Key)
    user_id = access_token["user_id"]
    expiration = access_token["exp"]
    if expiration < datetime.now(timezone.utc).timestamp():
        raise HTTPException(status_code=409, detail="Please Login Again")
    else:
        user = get_user_by_id(user_id)
        return user


def create_access_token(data_given: dict, expire_time_given: timedelta | None = None):
    expires_at = datetime.now(timezone.utc) + (
        expire_time_given if expire_time_given else timedelta(minutes=15)
    )
    data_given.update({"exp": expires_at})
    access_token = jwt.encode(data_given, Secret_Key, algorithm=Algorithm)
    return access_token


def create_refresh_token(user_id, expire_time_given: timedelta | None = None):
    expires_at = datetime.now(timezone.utc) + (
        expire_time_given if expire_time_given else timedelta(days=7)
    )
    data = {"user_id": user_id, "exp": expires_at}
    refresh_token = jwt.encode(data, Secret_Key, algorithm=Algorithm)
    token = add_refresh_token(
        refresh_token, datetime.now(timezone.utc), expires_at, user_id
    )
    return refresh_token


def validate_refresh_token(refresh_token):
    token_db = get_refresh_token_db(refresh_token)
    if not token_db:
        raise HTTPException(status_code=401, detail="Credientials Not Valid")
    else:
        try:
            data = jwt.decode(refresh_token, Secret_Key)
            return data["user_id"]
        except:
            raise HTTPException(
                status_code=401, detail="Refresh Token Expired Please Login again"
            )


def generate_new_access(refresh_token: str):
    user_id = validate_refresh_token(refresh_token)
    data = {"user_id": user_id}
    access_token = create_access_token(data)
    return access_token
