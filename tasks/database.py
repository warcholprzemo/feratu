import os
from dataclasses import dataclass

import motor.motor_asyncio
from bson.objectid import ObjectId


MONGODB_PASSWORD = os.getenv("MONGODB_PASSWORD")
MONGO_DETAILS = f"mongodb+srv://warcholprzemo:{MONGODB_PASSWORD}@cluster0.6bzyr4c.mongodb.net/?retryWrites=true&w=majority"
# MONGO_DETAILS = "mongodb://mongoservice:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.feratu

tasks_collection = database.get_collection("tasks")


@dataclass
class UpdateStatus:
    updated: bool
    message: str


@dataclass
class DeleteStatus:
    deleted: bool
    message: str


def task_helper(task) -> dict:
    return {
        "id": str(task["_id"]),
        "created": task["created"],
        "finished": task["finished"],
        "title": task["title"],
        "description": task["description"],
        "done": task["done"],
        "comments": task.get("comments"),
    }


async def retrieve_tasks() -> list:
    tasks = []
    async for task in tasks_collection.find():
        tasks.append(task_helper(task))
    return tasks


async def add_task(task_data: dict) -> dict:
    task = await tasks_collection.insert_one(task_data)
    new_task = await tasks_collection.find_one({"_id": task.inserted_id})
    return task_helper(new_task)


async def get_task(task_id: str) -> dict:
    task = await tasks_collection.find_one({"_id": ObjectId(task_id)})
    return task_helper(task)


async def update_task(task_id: str, task_data: dict, new_comment: dict) -> UpdateStatus:
    if new_comment:
        original_task = await get_task(task_id)
        comments = original_task["comments"] or []
        comments.append(new_comment)
        task_data["comments"] = comments

    update_result = await tasks_collection.update_one(
        {"_id": ObjectId(task_id)}, {"$set": task_data}
    )
    if update_result.matched_count:
        return UpdateStatus(
            True,
            f"Task {task_id} updated correctly ({update_result.modified_count} rows)",
        )
    return UpdateStatus(False, f"Task {task_id} not found")


async def delete_task(task_id: str) -> DeleteStatus:
    delete_result = await tasks_collection.delete_one({"_id": ObjectId(task_id)})
    if delete_result.deleted_count:
        return DeleteStatus(True, f"Task {task_id} deleted correctly")
    return DeleteStatus(False, f"Task {task_id} not found")
