from pydantic import BaseModel, EmailStr
from typing import Optional

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    user_id: int
    token: str
    expires_in: int
    login_status: str
    token_type: str = "bearer"
