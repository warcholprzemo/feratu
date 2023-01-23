from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Task(BaseModel):
    created: datetime
    finished: datetime | None = None
    title: str
    description: str = ""
    done: bool = False


@app.get("/tasks/")
async def tasks() -> list[Task]:
    return [
        Task(
            created=datetime(2023, 1, 1),
            finished=datetime(2023, 1, 8),
            title="Buy new bookshelf",
            done=True,
        )
    ]


@app.post("/tasks/add/")
async def add_task(task: Task) -> Task:
    return task
