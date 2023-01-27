from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder

from .database import add_task, retrieve_tasks
from .models import Task


app = FastAPI()


@app.get("/")
async def hello():
    return {"Message": "Hello World"}


@app.get("/tasks/")
async def tasks_view() -> list[Task]:
    tasks = await retrieve_tasks()
    return tasks


@app.post("/tasks/add/")
async def add_task_view(task: Task) -> Task:
    task_data = jsonable_encoder(task)
    new_task = await add_task(task_data)
    return new_task
