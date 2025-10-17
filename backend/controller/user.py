from controller.auth import (
    create_access_token,
    authenticate_user,
    create_refresh_token,
    generate_new_access,
)
from fastapi import APIRouter, Depends, HTTPException
from controller.schema import User
from model.auth import create_user, get_user_by_email
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated


app = APIRouter(prefix="/user")


@app.post("/create")
def create_user_request(user_data: User):
    user = create_user(
        user_data.name, user_data.email, user_data.password, user_data.is_supervisor
    )
    access_token = create_access_token({"user_id": user.id})
    refresh_token = create_refresh_token(user.id)
    return {"access_token": access_token, "refresh_token": refresh_token}


@app.post("/login")
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


@app.get("/me")
def get_user_info(user: Annotated[dict, Depends(authenticate_user)]):
    return {"user": user}


@app.post("/generate-access-token")
def generate_access_token(data: dict):
    refresh_token = data["refresh_token"]
    access_token = generate_new_access(refresh_token)
    return {"access_token": access_token, "type": "bearer"}
