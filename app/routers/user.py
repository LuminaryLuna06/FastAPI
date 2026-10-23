from fastapi import APIRouter, Depends

user_router = APIRouter(
    prefix="/user", tags=["user"], responses={404: {"user": "Not found"}}
)


@user_router.get("/")
def main():
    return {"message": "Hello World"}


def get_user(role: str = "guest"):
    return {"role": role}


@user_router.get("/me")
def read_me(user=Depends(get_user)):
    return user


# @user_router.get("/{user_id}", status_code=404)
# def getUser(user_id: int):
#     raise HTTPException(status_code=404, detail="User not found")
