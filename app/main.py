from fastapi import APIRouter, FastAPI
from routers import user

app = FastAPI(title="Test FastAPI Structure")
router = APIRouter()
v1 = APIRouter(prefix="/api/v1")


v1.include_router(user.user_router)
app.include_router(v1)
