from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from serverapp.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String, unique=True, index=True)

    first_name = Column(String, index=True, default='')

    last_name = Column(String, index=True, default='')

    hashed_password = Column(String)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow())

    updated_at = Column(DateTime, default=datetime.utcnow())


class AuthToken(Base):
    __tablename__ = "auth_tokens"

    id = Column(Integer, primary_key=True, index=True)

    token = Column(String, index=True)

    user_id = Column(Integer, ForeignKey(User.id), name="user_token", index=True)

    created_at = Column(DateTime, default=datetime.utcnow())

    updated_at = Column(DateTime, default=datetime.utcnow())

    expired_at = Column(DateTime)

