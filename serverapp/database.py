from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql://crypto:3xaG3adhgDadXAxDBADgAA36Xda7B@127.0.0.1:5432/fastapi"

# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}) only for sqllite
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
