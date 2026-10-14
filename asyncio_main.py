import asyncio
import time
from enum import Enum

from fastapi import FastAPI

# Create an instance of FastAPI
app = FastAPI()


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


# @ is a decorative, it take the function right under it.
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/post/{post_id}")
async def newPost(post_id: int):
    return {"post_id": post_id}


@app.get("/models/{model_name}")
async def getModel(model_name: ModelName):
    return {"model_name": model_name}


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


# Bad async make the server unable to serve other task, while good async allow quick to run right away, it doesnt block other task.
@app.get("/bad_async")
async def bad_async():
    time.sleep(5)
    return {"msg": "bad async"}


@app.get("/good_async")
async def good_async():
    await asyncio.sleep(5)
    return {"msg": "good async"}


@app.get("/quick")
async def quick():
    return {"msg": "Quick"}


@app.get("/hello")
async def main():
    print("hello")
    await asyncio.sleep(1)
    print("world")


async def say_after(time: int, what: str):
    await asyncio.sleep(time)
    print(what)
    return True


# There are 2 way of creating task with asyncio: asyncio.create_task() or asyncio.TaskGroup.create_task() (TaskGroup is a class of asyncio)
@app.get("/say")
async def say():
    task1 = asyncio.create_task(say_after(1, "hello"))
    task2 = asyncio.create_task(say_after(2, "hello"))

    print(f"started at {time.strftime('%X')}")

    await task1
    await task2

    print(f"finished at {time.strftime('%X')}")


# TaskGroup
@app.get("/say2")
async def say2():
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(say_after(1, "Hello"))
        task2 = tg.create_task(say_after(2, "World"))
    print(f"Both tasks have completed now: {task1.result()}, {task2.result()}")


# Gather run tasks concurrently. That mean the whole gather will take 4 secs to finish.
@app.get("/gather")
async def gather():
    await say_after(1, "Hello")

    await asyncio.gather(say_after(2, "World"), asyncio.sleep(4))


def blocking_io():
    print(f"start blocking_io at {time.strftime('%X')}")
    # Note that time.sleep() can be replaced with any blocking
    # IO-bound operation, such as file operations.
    time.sleep(1)
    print(f"blocking_io complete at {time.strftime('%X')}")


# To_thread() send blocking I/O to another thread so it doesnt block the main thread.
@app.get("/thread")
async def thread():
    print(f"started main at {time.strftime('%X')}")

    await asyncio.gather(asyncio.to_thread(blocking_io), asyncio.sleep(1))

    print(f"finished main at {time.strftime('%X')}")


async def eternity():
    # Sleep for one hour
    await asyncio.sleep(3600)
    print("yay!")


@app.get("/eternity")
async def testEternity():
    try:
        await asyncio.wait_for(eternity(), timeout=1.0)
    except TimeoutError:
        print("Timeout")
