from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from serverapp.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(String, unique=True, index=True)

    hashed_password = Column(String)

    is_active = Column(Boolean, default=True)

    created_at = Column(DateTime, default=datetime.utcnow())

    updated_at = Column(DateTime, default=datetime.utcnow())

