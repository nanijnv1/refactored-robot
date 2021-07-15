from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime


class UserBaseSchema(BaseModel):
    email: str


class UserCreateSchema(UserBaseSchema):
    password: str


class UserSchema(UserBaseSchema):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
