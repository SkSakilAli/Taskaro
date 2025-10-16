from fastapi import Depends, FastAPI, HTTPException
from model.schema import Base
from model.config import engine
from model.auth import create_user, get_user_by_email
from controller.auth import (
    create_access_token,
    authenticate_user,
    create_refresh_token,
    Secret_Key,
    Oauth_scheme,
    generate_new_access,
)
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from typing import Annotated
from model.schema import create_db

create_db()
app = FastAPI()


class Response_token:
    token: str


@app.post("/user/create")
def create_user_request(user_data: dict):
    user = create_user(user_data["name"], user_data["email"], user_data["password"])
    access_token = create_access_token({"user_id": user.id})
    refresh_token = create_refresh_token(user.id)
    return {"access_token": access_token, "refresh_token": refresh_token}


@app.post("/user/login")
def user_login_request(request_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = get_user_by_email(request_data.username)
    if user:
        access_token = create_access_token({"user_id": user.id})
        refresh_token = create_refresh_token(user.id)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }
    else:
        raise HTTPException(status_code=404, detail="User does not exist")


@app.get("/user/me")
def get_user_info(user: Annotated[dict, Depends(authenticate_user)]):
    return {"user": user}


@app.post("/user/generate-access-token")
def generate_access_token(data: dict):
    refresh_token = data["refresh_token"]
    access_token = generate_new_access(refresh_token)
    return {"access_token": access_token, "type": "bearer"}


@app.get("/tasks")
def get_my_task_request(user_id: Annotated[int, Depends(authenticate_user)]):
    tasks = get_task_by_user_id(user_id)
    return {"tasks": ""}


@app.post("/createtask")
def create_task_request(
    user: Annotated[dict, Depends(authenticate_user)], task_data: dict
):
    pass
