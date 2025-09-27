import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()


URL_DATABASE = os.getenv("URL_DATABASE")

if not URL_DATABASE:
    raise ValueError("❌ URL_DATABASE is not set in .env file")

#Create SQLAlchemy engine
engine = create_engine(URL_DATABASE)

#Session factory for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base class for SQLAlchemy models
Base = declarative_base()

#Dependency function for getting a session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
