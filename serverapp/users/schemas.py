from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime


class UserBaseSchema(BaseModel):
    email: str


class UserCreateSchema(UserBaseSchema):
    password: str
    first_name: str
    last_name: str


class UserLoginSchema(UserBaseSchema):
    password: str


class UserSchema(UserBaseSchema):
    id: int
    first_name: str
    last_name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str = None
