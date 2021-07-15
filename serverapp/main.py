from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import sys

# from . import crud, models, schemas
from .database import SessionLocal, engine, Base
from .users.schemas import UserSchema, UserCreateSchema, UserBaseSchema
from .users.views import get_user_by_email, get_user, get_users, create_user

Base.metadata.create_all(bind=engine)
app = FastAPI()

print(sys.getrecursionlimit())



# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", )
def welcome(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # users = get_users(db, skip=skip, limit=limit)
    return "Welcome"

@app.post("/users/", response_model=UserSchema)
def register_user(user: UserCreateSchema, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, user=user)


@app.get("/users/", response_model=List[UserSchema])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=UserSchema)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
