from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from schemas.auth import LoginInput, LoginResponse, RefreshTokenInput
from services.auth import login_user, refresh_access_token

router = APIRouter(tags=["auth"])


@router.post("/login", response_model=LoginResponse)
async def login(payload: LoginInput):
    return await login_user(payload.email, payload.password)


@router.post("/login/swagger", response_model=LoginResponse)
async def login_swagger(form_data: OAuth2PasswordRequestForm = Depends()):
    return await login_user(form_data.username, form_data.password)


@router.post("/refresh")
async def refresh_token(payload: RefreshTokenInput):
    return await refresh_access_token(payload.refresh_token)

