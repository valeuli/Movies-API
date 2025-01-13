from typing import Optional

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: Optional[str] = None
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
