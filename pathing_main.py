from fastapi import FastAPI, Response, status
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    id: int
    title: str
    created_at: str


posts: list[Post] = []


@app.get("/")
def home():
    return {"message": "Welcome home"}


# Response Headers
@app.get("/posts")
def getPosts(response: Response):
    response.headers["X-Cat-Dog"] = "alone in the world"
    return {"data": posts}


# Custom HTTP Status Code
@app.post("/new", status_code=status.HTTP_201_CREATED)
def addPost(post: Post):
    if post:
        posts.append(post)
    return {"message": "Post Created", "data": post}


@app.put("/edit")
async def editPost(id: int, title: str):
    return {"message": f"Post {id} editted", "data": title}


# Path Parameters: /items/{item_id}
@app.get("/posts/{post_id}")
def getPost(post_id: int):
    # List comprehension
    post = next(post for post in posts if post.id == post_id)
    if post:
        return {"success": True, "data": post}
    return {"message": "Post not found"}


# Advance type annotations (Path validation):
# async def read_post(post_id: Annotated[int, Path(ge=1, le=9999)]):
#     return {"post_id": post_id}


# Query Parameters: /items?id=...&limit=20
