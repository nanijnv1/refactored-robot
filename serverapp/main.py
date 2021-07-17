from typing import List

from fastapi import Depends, FastAPI, HTTPException, Response
from sqlalchemy.orm import Session
import sys

# from . import crud, models, schemas
from .database import SessionLocal, engine, Base
from .users.schemas import UserSchema, UserCreateSchema, UserBaseSchema
from .users.views import get_user_by_email, get_user, get_users, create_user, \
    check_username_password, create_access_token
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, HTTPBasic


Base.metadata.create_all(bind=engine)
app = FastAPI()

my_secret_key = "pleaSeDoN0tKillMyC_at"
security = HTTPBasic()
# auth_handler = Authorization(my_secret_key)


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


@app.post("/login")
def login(user: UserCreateSchema, response: Response, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user is None:
        raise HTTPException(status_code=400, detail="Username not existed")
    else:
        is_password_correct = check_username_password(db, user)
        if not is_password_correct:
            raise HTTPException(status_code=400, detail="Password is not correct")
        else:
            access_token = create_access_token(data={"sub": user.email})
            response.headers["Bearer"] = access_token
            return user


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
