# database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

# SQLite database file
DATABASE_URL = "sqlite:///./shortener.db"

# Create engine (connection layer)
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # required for SQLite
)

# Create session (used to talk to DB)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()  # 👈 important for ORM models