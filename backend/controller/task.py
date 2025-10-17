from model.task import add_task_db, get_task_by_user_id, mark_as_complete_db
from fastapi import APIRouter, Depends, HTTPException
from controller.auth import authenticate_user
from controller.schema import Create_Task, User
from typing import Annotated

app = APIRouter(prefix="/tasks")


@app.get("/")
def get_my_task_request(user: Annotated[User, Depends(authenticate_user)]):
    tasks = get_task_by_user_id(user.id)
    return {"tasks": tasks}


@app.post("/create")
def create_task_request(
    user: Annotated[User, Depends(authenticate_user)], task_data: Create_Task
):
    user_id = user.id
    title = task_data.title
    assigned_by = None
    task = add_task_db(user_id, title, assigned_by)
    return task


@app.get("/markcomplete/{task_id}")
def mark_as_complete(user: Annotated[User, Depends(authenticate_user)], task_id: int):
    user_tasks = get_task_by_user_id(user.id)
    # return user_tasks
    for task in user_tasks:
        if task.id == task_id:
            return mark_as_complete_db(task_id)
    raise HTTPException(status_code=400, detail="Task Not Found")
