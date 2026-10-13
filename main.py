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
