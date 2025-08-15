from fastapi import APIRouter
from schemas.auth import LoginInput, LoginResponse
from services.auth import login_user

router = APIRouter(tags=["auth"])

@router.post("/login", response_model=LoginResponse)
async def login(payload: LoginInput):
    return await login_user(payload.email, payload.password)
