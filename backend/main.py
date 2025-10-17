from fastapi import FastAPI
from controller.user import app as user_router
from controller.task import app as task_router
from controller.subordinate import app as subordinate_router

app = FastAPI()


app.include_router(user_router)
app.include_router(task_router)
app.include_router(subordinate_router)
