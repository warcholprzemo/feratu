from datetime import datetime

from pydantic import BaseModel


class Task(BaseModel):
    created: datetime
    finished: datetime | None = None
    title: str
    description: str = ""
    done: bool = False

    class Config:
        schema_extra = {
            "example": {
                "created": datetime(2023, 1, 1, 7, 10, 56),
                "finished": datetime(2023, 1, 8, 23, 55, 11),
                "title": "Buy new bookshelf",
                "description": "Bought in Agata Meble",
                "done": True,
            }
        }
