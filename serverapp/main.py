from typing import List

from fastapi import Depends, FastAPI, HTTPException, Response
from sqlalchemy.orm import Session
import sys

# from . import crud, models, schemas
from .database import SessionLocal, engine, Base
from .users.schemas import UserSchema, UserCreateSchema, UserBaseSchema, UserLoginSchema
from .users.views import get_user_by_email, get_user, get_users, create_user, \
    check_username_password, create_access_token, validate_token
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, HTTPBasic, HTTPBasicCredentials

Base.metadata.create_all(bind=engine)
app = FastAPI()

auth = HTTPBearer()


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


@app.post("/register/", response_model=UserSchema)
def register_user(user: UserCreateSchema, response: Response, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    else:
        new_user = create_user(db=db, user=user)
        access_token = create_access_token(data={"email": user.email, 'name': new_user.first_name, 'id': new_user.id},
                                           db=db, user=new_user)
        response.headers["Token"] = access_token
    return new_user


@app.post("/login/")
def login(user: UserLoginSchema, response: Response, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user is None:
        raise HTTPException(status_code=400, detail="Username not existed")
    else:
        is_password_correct = check_username_password(db, user)
        if not is_password_correct:
            raise HTTPException(status_code=400, detail="incorrect password")
        else:
            access_token = create_access_token(data={"email": user.email, 'name': db_user.first_name, 'id': db_user.id},
                                               db=db, user=db_user)
            response.headers["Token"] = access_token
            return user


@app.get("/users/", response_model=List[UserSchema], )
def read_users(skip: int = 0, limit: int = 100, authorization: HTTPAuthorizationCredentials = Depends(auth),
               db: Session = Depends(get_db)):
    validate_token(db, authorization.credentials)
    users = get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=UserSchema)
def read_user(user_id: int, db: Session = Depends(get_db), authorization: HTTPAuthorizationCredentials = Depends(auth)):
    validate_token(db, authorization.credentials)
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
