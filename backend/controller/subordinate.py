from fastapi import APIRouter, HTTPException, Depends
from model.task import add_task_db, get_task_by_user_id
from model.supervisor import (
    check_if_supervisor,
    add_subordinate_db,
    get_subordinate_db,
    check_supervisor_subordinate_relation,
)
from controller.schema import Add_Subordinate, Create_Task
from controller.auth import authenticate_user
from controller.schema import User
from typing import Annotated


app = APIRouter(prefix="/subordinate")


@app.post("/add")
def add_subordinate(
    user: Annotated[User, Depends(authenticate_user)],
    sub_ordinate_data: Add_Subordinate,
):
    if check_if_supervisor(user.id):
        return add_subordinate_db(user.id, sub_ordinate_data.email)
    else:
        raise HTTPException(status_code=400, detail="You are not Supervisor")


@app.get("/")
def get_subordinates_detail(user: Annotated[User, Depends(authenticate_user)]):
    return get_subordinate_db(user.id)


@app.post("/addtask")
def add_subordinate_task(
    user: Annotated[User, Depends(authenticate_user)],
    subordinate_id: int,
    task_data: Create_Task,
):
    if check_supervisor_subordinate_relation(user.id, subordinate_id):
        user_id = subordinate_id
        title = task_data.title
        assigned_by = user.id
        task = add_task_db(user_id, title, assigned_by)
        return task


@app.get("/gettask")
def get_subordinate_task(
    user: Annotated[User, Depends(authenticate_user)], subordinate_id: int
):
    if check_supervisor_subordinate_relation(user.id, subordinate_id):
        return get_task_by_user_id(subordinate_id)
