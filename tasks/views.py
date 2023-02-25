from fastapi import FastAPI, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

from .database import add_task, delete_task, get_task, retrieve_tasks, update_task
from .models import FullTask, Task


app = FastAPI()

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def hello():
    return {"Message": "Hello World"}


@app.get("/tasks/")
async def tasks_view() -> list[FullTask]:
    tasks = await retrieve_tasks()
    return tasks


@app.post("/tasks/")
async def add_task_view(task: Task) -> Task:
    task_data = jsonable_encoder(task)
    new_task = await add_task(task_data)
    return new_task


@app.get("/tasks/{task_id}")
async def get_task_view(task_id: str) -> Task:
    task = await get_task(task_id)
    return task


@app.put("/tasks/{task_id}")
async def update_task_view(task_id: str, task: Task, response: Response) -> dict:
    # TODO replace Task -> UpdateTask with all optional fields
    update_status = await update_task(task_id, task.dict())
    if update_status.updated:
        return {"info": update_status.message}

    response.status_code = status.HTTP_404_NOT_FOUND
    return {"error": update_status.message}


@app.delete("/tasks/{task_id}")
async def delete_task_view(task_id: str, response: Response) -> dict:
    delete_status = await delete_task(task_id)
    if delete_status.deleted:
        return {"info": delete_status.message}

    response.status_code = status.HTTP_404_NOT_FOUND
    return {"error": delete_status.message}
