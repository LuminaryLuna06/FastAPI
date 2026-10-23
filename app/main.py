from fastapi import APIRouter, FastAPI, Header, HTTPException, status
from routers import test_db, user

app = FastAPI(title="Test FastAPI Structure")
router = APIRouter()


# API Key validation
VALID_API_KEYS = {"secret_key_123", "internal_service_key_abc"}


async def verify_api_key(
    x_api_key: str = Header(..., description="API Key to authenticate"),
):
    if x_api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="API Key is not valid"
        )
    return x_api_key


# v1 = APIRouter(prefix="/api/v1", dependencies=[Depends(verify_api_key)])
v1 = APIRouter(prefix="/api/v1")


v1.include_router(user.user_router)
v1.include_router(test_db.test_db)
app.include_router(v1)
