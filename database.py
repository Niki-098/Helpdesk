import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Load environment variables from .env file
load_dotenv()

# Example in .env:
# URL_DATABASE=postgresql://postgres:1234@localhost:5432/AI_Interviewer

# Read database URL directly from environment
URL_DATABASE = os.getenv("URL_DATABASE")

if not URL_DATABASE:
    raise ValueError("❌ URL_DATABASE is not set in .env file")

# Create SQLAlchemy engine
engine = create_engine(URL_DATABASE)

# Session factory for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models (if you want to define raw models)
Base = declarative_base()

# Dependency function for getting a session (useful in scripts/FastAPI)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
