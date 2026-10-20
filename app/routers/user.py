from fastapi import APIRouter

user_router = APIRouter(
    prefix="/user", tags=["user"], responses={404: {"user": "Not found"}}
)


@user_router.get("/")
def main():
    return {"message": "Hello World"}


# @user_router.get("/{user_id}", status_code=404)
# def getUser(user_id: int):
#     raise HTTPException(status_code=404, detail="User not found")
