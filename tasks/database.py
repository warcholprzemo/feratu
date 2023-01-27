import motor.motor_asyncio

MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.feratu

tasks_collection = database.get_collection("tasks")


def task_helper(task) -> dict:
    return {
        "id": str(task["_id"]),
        "created": task["created"],
        "finished": task["finished"],
        "title": task["title"],
        "description": task["description"],
        "done": task["done"],
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
