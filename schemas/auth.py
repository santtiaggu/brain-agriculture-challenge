from pydantic import BaseModel, EmailStr

class LoginInput(BaseModel):
    email: EmailStr
    password: str

class UserInfo(BaseModel):
    id: int
    email: EmailStr
    first_name: str
    last_name: str
    admin: bool
    phone: str | None = None

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserInfo

class RefreshTokenInput(BaseModel):
    refresh_token: str
