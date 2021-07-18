from sqlalchemy.orm import Session
import bcrypt
from .schemas import UserCreateSchema, UserSchema, UserLoginSchema
from .models import User, AuthToken
from datetime import timedelta, datetime
import jwt


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreateSchema):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), salt)
    db_user = User(email=user.email, hashed_password=hashed_password.decode('utf-8'), first_name=user.first_name,
                   last_name=user.last_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def check_username_password(db: Session, user: UserLoginSchema):
    db_user = get_user_by_email(db, email=user.email)
    return bcrypt.checkpw(user.password.encode('utf-8'), db_user.hashed_password.encode('utf-8'))


def create_access_token(*, data: dict, expires_delta: timedelta = None, db: Session, user):
    secret_key = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    algorithm = "HS256"
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = -1
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    add_token_to_db(db, encoded_jwt, user)
    return encoded_jwt


async def add_token_to_db(db: Session, token, user):
    db_token = AuthToken(token=token, user_id=user.id)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
