from datetime import datetime

from pydantic import BaseModel


class Comment(BaseModel):
    author: str
    message: str


class Task(BaseModel):
    created: datetime | None = None
    finished: datetime | None = None
    title: str
    description: str = ""
    done: bool = False
    comments: list[Comment] | None = None

    class Config:
        schema_extra = {
            "example": {
                "created": datetime(2023, 1, 1, 7, 10, 56),
                "finished": datetime(2023, 1, 8, 23, 55, 11),
                "title": "Buy new bookshelf",
                "description": "Bought in Agata Meble",
                "done": True,
                "comments": [
                    {
                        "author": "ziutek",
                        "message": "good choice",
                    }
                ],
            }
        }


class UpdateTask(BaseModel):
    title: str
    description: str
    done: bool
    finished: datetime | None = None
    comments: list[Comment] | None = None
    new_comment: Comment | None = None


class FullTask(Task):
    id: str
